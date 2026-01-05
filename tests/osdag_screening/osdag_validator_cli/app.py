# osdag_validator_cli/app.py
"""
Stable FastAPI API for osdag-validator.

This module uses the Validator class directly (via get_validator()) and keeps
HTTP handlers simple and explicit (no CLI wrapper invocation) to avoid arg-mismatch.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Any, Optional

from osdag_validator_cli.cli import get_validator, as_number_if_possible, run_batch_file, run_command

app = FastAPI(title="Osdag Validator API", version="1.0")


class ValidateRequest(BaseModel):
    command: str = Field(..., example="fu")
    args: List[str] = Field(default_factory=list)
    format: Optional[str] = "json"


class ValidateResponse(BaseModel):
    ok: bool
    command: str
    args: List[str]
    result: Any


@app.get("/health")
def health():
    return {"ok": True, "name": "osdag-validator-api", "version": "1.0"}


@app.post("/validate", response_model=ValidateResponse)
def validate(req: ValidateRequest):
    try:
        v = get_validator()
    except ImportError as e:
        raise HTTPException(status_code=500, detail=str(e))

    cmd = req.command.lower().strip()
    args = req.args or []

    try:
        # ---- FU ----
        if cmd == "fu":
            if len(args) < 1:
                raise HTTPException(400, "fu requires 1 argument")
            value = as_number_if_possible(args[0])
            out = v.validate_fu(value)
            return ValidateResponse(ok=True, command=cmd, args=args, result=out)

        # ---- FY ----
        if cmd == "fy":
            if len(args) < 1:
                raise HTTPException(400, "fy requires 1 argument")
            value = as_number_if_possible(args[0])
            out = v.validate_fy(value)
            return ValidateResponse(ok=True, command=cmd, args=args, result=out)

        # ---- FU-FY ----
        if cmd in ("fu-fy", "fufy"):
            if len(args) < 2:
                raise HTTPException(400, "fu-fy requires 2 arguments")
            fu = as_number_if_possible(args[0])
            fy = as_number_if_possible(args[1])
            out = v.validate_fu_fy(fu, fy)
            return ValidateResponse(ok=True, command=cmd, args=args, result=out)

        # ---- TF (optional method on Validator) ----
        if cmd == "tf":
            if len(args) < 1:
                raise HTTPException(400, "tf requires 1 argument")
            value = as_number_if_possible(args[0])
            out = getattr(v, "validate_tf", lambda x: False)(value)
            return ValidateResponse(ok=True, command=cmd, args=args, result=out)

        # ---- bolt / plate are forwarded if Validator implements them ----
        if cmd == "bolt":
            if len(args) < 2:
                raise HTTPException(400, "bolt requires size and grade")
            out = getattr(v, "validate_bolt", lambda s,g: False)(args[0], args[1])
            return ValidateResponse(ok=True, command=cmd, args=args, result=out)

        if cmd == "plate":
            if len(args) < 2:
                raise HTTPException(400, "plate requires thickness and width")
            t = as_number_if_possible(args[0])
            w = as_number_if_possible(args[1])
            out = getattr(v, "validate_plate", lambda a,b: False)(t,w)
            return ValidateResponse(ok=True, command=cmd, args=args, result=out)

        # ---- batch (server-side batch runner) ----
        if cmd == "batch":
            if len(args) < 1:
                raise HTTPException(status_code=400, detail="batch requires path argument in args[0]")
            path = args[0]
            out = run_batch_file(path)
            return ValidateResponse(ok=True, command=cmd, args=args, result=out)

        # unsupported
        raise HTTPException(status_code=400, detail=f"Unsupported command: {cmd}")

    except HTTPException:
        raise
    except Exception as e:
        # Internal error
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")
