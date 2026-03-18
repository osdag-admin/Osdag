# Osdag IFC Generator Status Report

## 1. Introduction
The Osdag IFC Generator is a critical module engineered to export Osdag's highly detailed 3D structural steel connections into the Industry Foundation Classes (IFC) format. The main objective of this tool is to provide seamless interoperability with prominent commercial BIM applications—such as Revit, Tekla, and Archicad—while rigidly adhering to LOD 500 standards for as-built and field-verified modeling. By reliably extracting precise geometries, physical bolt hole voids, and comprehensive engineering metadata, the generator ensures that essential structural design data is completely preserved and functional during the BIM handover process.

## 2. File Breakdown: `export_ifc` Directory
The `export_ifc` / `export_ifc_v2` module is structured into distinct, modular scripts that separate data extraction from IFC file generation:
* **`__init__.py`**: Standard Python package initialization file.
* **`cad_extraction.py`**: Contains reusable CAD extraction utilities. It is responsible for parsing complex OSDAG GUI objects and safely extracting lists of simple physical primitives (Members, Plates, Bolts, Welds). It serializes these objects into lightweight, JSON-compatible dictionaries, effectively stripping away heavy OpenCASCADE geometry dependencies.
* **`geometry_mapper.py`**: The core geometric engine. It translates local coordinates and dimensions from Osdag into explicit buildingSMART IFC geometries. It generates 2D profiles (`IfcArbitraryClosedProfileDef`), extrusions (`IfcExtrudedAreaSolid`), robust hardware instances (`IfcMappedItem`), and handles complex boolean cutting operations for bolt voids.
* **`ifc_generator.py`**: The primary orchestration class (`OsdagIfcExporter`). It initializes the IFC file environment, establishes the mandatory spatial hierarchy sequence (`Project` → `Site` → `Building` → `Storey`), manages deterministic GUID generation, and orchestrates the geometric and metadata mappers to assemble the final product.
* **`metadata_mapper.py`**: Handles semantic data injection. It maps engineering specifics (material grades, profiles, capacities, loads, design codes) into custom buildingSMART property sets (`Pset_OsdagDesignData`). It also groups the separate physical items into a unified structural `IfcElementAssembly`.
* **`subprocess_ifc_exporter.py`**: An independent execution script designed to be run as an isolated subprocess. It ingests the serialized JSON CAD payload, reconstructs lightweight object mockups, and triggers the `OsdagIfcExporter`. This architectural isolation guarantees that any `ifcopenshell` faults or high-memory operations do not crash the main Osdag PyQt GUI.

## 3. Detailed IFC Generation Pipeline
The end-to-end process of generating an IFC file from an Osdag connection model follows a strict, isolated pipeline:

1. **Trigger & Extraction**: The user requests an IFC export from the Osdag UI. The system triggers `cad_extraction.py`, which utilizes a unified dispatcher to parse the active CAD Module based on its connection class (e.g., `FinPlateCAD`). It iterates through the class properties to categorize and extract all visual parts into logical structural groups (members, plates, fasteners, welds).
2. **Serialization & Offloading**: To avoid crashing the GUI with heavy standard libraries, `cad_extraction.py` serializes the categorized CAD parts and the engineering metadata into a flat JSON dictionary. This JSON payload is temporarily written to disk.
3. **Subprocess Dispatch**: The main Osdag GUI thread spawns a separate background process targeting `subprocess_ifc_exporter.py`, passing the newly created JSON file path as a command-line argument.
4. **Data Rehydration**: The subprocess runs, reads the JSON payload, and dynamically reconstructs lightweight Python object namespaces that mimic the original CAD elements' numeric properties, but without the baggage of PySide or OpenCASCADE.
5. **IFC Initialization**: The `OsdagIfcExporter` (`ifc_generator.py`) is instantiated. It generates a blank file using the specified schema (e.g., `IFC2X3`), defines the standard unit assignments, and builds the baseline spatial project hierarchy.
6. **Geometry Construction**: The exporter loops through the structural groups, passing each item to `GeometryMapper` (`geometry_mapper.py`):
    * **Beams & Plates**: Mapped to `IfcExtrudedAreaSolid`.
    * **Fasteners (Bolts, Nuts, Washers)**: Mapped once and instanced repetitively using `IfcMappedItem` to save file size.
    * **Voids**: For every bolt passing through a plate, `GeometryMapper` creates a cylindrical `IfcOpeningElement` and performs an `IfcRelVoidsElement` cut to generate true LOD 500 physical holes.
7. **Metadata Binding**: As geometries are finalized, `MetadataMapper` (`metadata_mapper.py`) generates `Pset_OsdagDesignData` property sets containing the joint's design loads, capacities, and material traits, binding them to the respective 3D entities.
8. **Assembly & Finalization**: All connection components are aggregated into a top-level `IfcElementAssembly` (representing the joint as a whole single part) and fixed to the Building Storey. The underlying `ifcopenshell` engine writes the complete data tree to the desired `.ifc` output path, and the subprocess gracefully exits.

## 4. Current Wrapper Capabilities
The latest iteration of the IFC Wrapper (`export_ifc`) has achieved substantial milestones in terms of geometric fidelity and structural detailing:
* **Extensive Connection Support**: Advanced CAD extraction logic cleanly identifies and processes 28 explicit connection classes. This robust dispatcher seamlessly supports Simple Plated Joints, Shear Connections, Base Plates, Moment Connections (End Plate & Cover Plate architectures), and Truss/Tension networks.
* **LOD 500 Geometry Mapping**: The internal `GeometryMapper` utilizes precise parametric IFC profiles (e.g., `IfcRectangleHollowProfileDef`, `IfcArbitraryClosedProfileDef`) for accurate programmatic definitions of structural members (I-Sections, Angles, Channels, Hollow Sections) and miscellaneous plates (Stiffeners, Gussets).
* **High-Fidelity Fastener Instancing**: Hardware items such as bolts, nuts, washers, and curved anchor bolts are meticulously modeled using `IfcMappedItem` for highly lightweight scaling. Furthermore, true boolean cut operations (`IfcOpeningElement`) are applied directly to connection plates to dynamically generate physical bolt hole voids.
* **Semantic Hierarchy and Metadata**: Exports formulate and maintain a rigorous spatial hierarchy (`Project` → `Site` → `Building` → `Storey`). The wrapper dynamically injects exhaustive engineering metadata—covering materials, load calculations, and design status—via the custom `Pset_OsdagDesignData` property set.
* **Stable Entity Tracking**: The system leverages mathematically deterministic GUID generation (UUIDv5) based on internal Osdag item identifiers. This ensures robust and stable model element tracking across multiple iterative exports.

## 5. Current Limitations
Despite the highly robust geometric modeling, the IFC Generator currently faces a few technical limitations that require resolution:
* **Flexural Member Export Instability**: Certain complex spatial configurations and orientations of flexural members occasionally result in internal topological mapping failures, which can yield empty or unopenable IFC bodies.
* **Dispatcher Mismatches**: Although largely mitigated, relying on dynamic Osdag connection modeling means legacy setups sometimes fail. Occasional mismatches between GUI abstraction classes (e.g., `FinPlateCAD`) and internal Osdag system definitions (e.g., `ColFlangeBeamWeb`) can still invoke partial geometry bypasses during CAD extraction.
* **Arbitrary Profile Deficiencies**: Heavy reliance on purely 2D point arrays (`IfcArbitraryClosedProfileDef`) for mapping complex custom stiffeners and asymmetric gusset plates can occasionally lead to inverted normal faces or "non-planar" warnings in strict external BIM validators.
* **Incomplete Standard Classifications**: While the geometric detailing meets LOD 500, the full integration of rigorous international classifications—such as OmniClass or Uniclass structural code tagging—remains partially hardcoded or unimplemented.

## 6. In Progress Tasks
To transition this generator tool to true production readiness and complete BIM compatibility, the following objectives are actively being pursued by the team:
* **Debugging Flexural Members**: We are actively investigating the `CommonDesignLogic` module and respective CAD extractors to resolve pipeline failures and topological errors specifically targeting complex flexural member CAD generation.
* **Expanding Property Sets**: Finalizing the `metadata_mapper.py` routines to ensure the automated and comprehensive translation of native Osdag metrics into standard buildingSMART Psets, beyond just the current custom dictionaries.
* **Testing and Interoperability Validation**: Conducting rigorous, environment-agnostic testing of generated IFC2x3 and IFC4 files to mathematically verify zero data loss when importing the structural setups into target BIM hubs like Revit and Tekla Structures.
* **CLI Integration**: Bridging the generation wrapper capabilities directly into the Osdag Command Line Interface (CLI). This will facilitate swift, automated batch BIM-model exports straight from raw `.osi` files without imposing GUI dependency on the end-user.
