import sys
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel, QSlider
from PySide6.QtCore import QTimer, Qt
import pyqtgraph.opengl as gl


class PSOVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Particle Swarm Optimization Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        
        # PSO parameters
        self.n_particles = 50
        self.w = 0.7  # inertia weight
        self.c1 = 1.5  # cognitive parameter
        self.c2 = 1.5  # social parameter
        self.bounds = [-5, 5]
        
        # Initialize particles
        self.positions = np.random.uniform(self.bounds[0], self.bounds[1], (self.n_particles, 3))
        self.velocities = np.random.uniform(-1.0, 1.0, (self.n_particles, 3))
        self.pbest_positions = self.positions.copy()
        self.pbest_scores = np.array([self.objective_function(p) for p in self.positions])
        self.gbest_position = self.pbest_positions[np.argmin(self.pbest_scores)]
        self.gbest_score = np.min(self.pbest_scores)
        
        # Trail history
        self.max_trail_length = 50
        self.trails = [[] for _ in range(self.n_particles)]
        
        self.iteration = 0
        self.running = False
        
        self.setup_ui()
        self.setup_timer()
        
    def objective_function(self, pos):
        """Rastrigin function - good for visualizing convergence"""
        x, y, z = pos
        A = 10
        return 3*A + (x**2 - A*np.cos(2*np.pi*x)) + \
               (y**2 - A*np.cos(2*np.pi*y)) + \
               (z**2 - A*np.cos(2*np.pi*z))
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 3D plot widget
        self.view = gl.GLViewWidget()
        self.view.setBackgroundColor('k')
        self.view.setCameraPosition(distance=20, elevation=30, azimuth=45)
        layout.addWidget(self.view)
        
        # Add grid
        grid = gl.GLGridItem()
        grid.setSize(x=10, y=10, z=10)
        grid.setSpacing(x=1, y=1, z=1)
        self.view.addItem(grid)
        
        # Add axes
        axis = gl.GLAxisItem()
        axis.setSize(x=6, y=6, z=6)
        self.view.addItem(axis)
        
        # Particle scatter plot (current positions)
        colors = np.zeros((self.n_particles, 4))
        colors[:, 0] = 1.0  # Red
        colors[:, 3] = 1.0  # Full alpha
        
        self.particles_plot = gl.GLScatterPlotItem(
            pos=self.positions,
            color=colors,
            size=10,
            pxMode=True
        )
        self.view.addItem(self.particles_plot)
        
        # Personal best positions
        pbest_colors = np.zeros((self.n_particles, 4))
        pbest_colors[:, 1] = 1.0  # Green
        pbest_colors[:, 3] = 0.3  # Semi-transparent
        
        self.pbest_plot = gl.GLScatterPlotItem(
            pos=self.pbest_positions,
            color=pbest_colors,
            size=6,
            pxMode=True
        )
        self.view.addItem(self.pbest_plot)
        
        # Global best marker
        self.gbest_plot = gl.GLScatterPlotItem(
            pos=np.array([self.gbest_position]),
            color=(0, 1, 1, 1),  # Cyan
            size=20,
            pxMode=True
        )
        self.view.addItem(self.gbest_plot)
        
        # Trail lines
        self.trail_items = []
        for i in range(self.n_particles):
            trail_item = gl.GLLinePlotItem(
                pos=np.array([[0, 0, 0]]),
                color=(1, 0.5, 0, 0.5),  # Orange with transparency
                width=1.5,
                antialias=True
            )
            self.view.addItem(trail_item)
            self.trail_items.append(trail_item)
        
        # Control panel
        control_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.toggle_simulation)
        self.start_btn.setFixedWidth(100)
        control_layout.addWidget(self.start_btn)
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_simulation)
        self.reset_btn.setFixedWidth(100)
        control_layout.addWidget(self.reset_btn)
        
        self.info_label = QLabel(f"Iteration: {self.iteration} | Best: {self.gbest_score:.4f}")
        self.info_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        control_layout.addWidget(self.info_label)
        
        control_layout.addStretch()
        
        # Speed slider
        control_layout.addWidget(QLabel("Speed:"))
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50)
        self.speed_slider.setFixedWidth(150)
        self.speed_slider.valueChanged.connect(self.update_speed)
        control_layout.addWidget(self.speed_slider)
        
        # Particle count label
        self.particle_label = QLabel(f"Particles: {self.n_particles}")
        control_layout.addWidget(self.particle_label)
        
        layout.addLayout(control_layout)
        
    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_pso)
        self.timer.setInterval(50)
        
    def update_speed(self):
        interval = int(101 - self.speed_slider.value())
        self.timer.setInterval(interval)
        
    def toggle_simulation(self):
        if self.running:
            self.timer.stop()
            self.start_btn.setText("Start")
            self.running = False
        else:
            self.timer.start()
            self.start_btn.setText("Pause")
            self.running = True
            
    def reset_simulation(self):
        self.timer.stop()
        self.running = False
        self.start_btn.setText("Start")
        self.iteration = 0
        
        # Reinitialize particles with more spread
        self.positions = np.random.uniform(self.bounds[0], self.bounds[1], (self.n_particles, 3))
        self.velocities = np.random.uniform(-1.0, 1.0, (self.n_particles, 3))
        self.pbest_positions = self.positions.copy()
        self.pbest_scores = np.array([self.objective_function(p) for p in self.positions])
        self.gbest_position = self.pbest_positions[np.argmin(self.pbest_scores)]
        self.gbest_score = np.min(self.pbest_scores)
        
        # Clear trails
        self.trails = [[] for _ in range(self.n_particles)]
        
        self.update_visualization()
        
    def update_pso(self):
        # PSO update equations
        r1 = np.random.random((self.n_particles, 3))
        r2 = np.random.random((self.n_particles, 3))
        
        cognitive = self.c1 * r1 * (self.pbest_positions - self.positions)
        social = self.c2 * r2 * (self.gbest_position - self.positions)
        
        self.velocities = self.w * self.velocities + cognitive + social
        
        # Limit velocity
        max_vel = 1.0
        self.velocities = np.clip(self.velocities, -max_vel, max_vel)
        
        # Update positions
        self.positions = self.positions + self.velocities
        
        # Apply boundary constraints
        self.positions = np.clip(self.positions, self.bounds[0], self.bounds[1])
        
        # Add current positions to trails
        for i in range(self.n_particles):
            self.trails[i].append(self.positions[i].copy())
            if len(self.trails[i]) > self.max_trail_length:
                self.trails[i].pop(0)
        
        # Evaluate and update personal best
        scores = np.array([self.objective_function(p) for p in self.positions])
        improved = scores < self.pbest_scores
        self.pbest_positions[improved] = self.positions[improved]
        self.pbest_scores[improved] = scores[improved]
        
        # Update global best
        min_idx = np.argmin(self.pbest_scores)
        if self.pbest_scores[min_idx] < self.gbest_score:
            self.gbest_position = self.pbest_positions[min_idx].copy()
            self.gbest_score = self.pbest_scores[min_idx]
        
        self.iteration += 1
        self.update_visualization()
        
    def update_visualization(self):
        # Update particle positions with color based on fitness
        scores = np.array([self.objective_function(p) for p in self.positions])
        normalized_scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-10)
        
        colors = np.zeros((self.n_particles, 4))
        colors[:, 0] = normalized_scores  # Red (bad)
        colors[:, 1] = 1 - normalized_scores  # Green (good)
        colors[:, 3] = 1.0  # Full alpha
        
        self.particles_plot.setData(pos=self.positions, color=colors)
        
        # Update personal best positions
        self.pbest_plot.setData(pos=self.pbest_positions)
        
        # Update global best position
        self.gbest_plot.setData(pos=np.array([self.gbest_position]))
        
        # Update trails
        for i, trail in enumerate(self.trails):
            if len(trail) > 1:
                trail_array = np.array(trail)
                self.trail_items[i].setData(pos=trail_array)
        
        # Update info label
        self.info_label.setText(
            f"Iteration: {self.iteration} | Best Score: {self.gbest_score:.4f} | "
            f"Pos: [{self.gbest_position[0]:.2f}, {self.gbest_position[1]:.2f}, {self.gbest_position[2]:.2f}]"
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PSOVisualizer()
    window.show()
    sys.exit(app.exec())