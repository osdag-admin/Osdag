
import numpy as np
import random

class IntelligentPSO:
    """
    Intelligent Particle Swarm Optimization
    Features:
    1. Discrete Variable Support: Snaps dimensions to nearest standard values provided in discrete_lists.
    2. Smart Boundary Handling: Clamps particles to valid bounds instead of random resampling.
    3. Soft Constraints: Returns high penalty instead of crashing/resetting.
    """
    def __init__(self, n_particles, dimensions, options, bounds, discrete_lists=None):
        self.n_particles = n_particles
        self.dimensions = dimensions
        self.bounds = bounds
        self.discrete_lists = discrete_lists # Dict: {index: [sorted_values]}
        
        # Options
        self.w = options.get('w', 0.5)      # Inertia
        self.c1 = options.get('c1', 0.5)    # Cognitive (Personal)
        self.c2 = options.get('c2', 0.5)    # Social (Global)
        self.debug = options.get('debug', False)

        # Initialize Swarm
        # Position: Continuous [0, 1] scale or Real scale? Real scale is easier for now.
        self.lb = np.array(bounds[0])
        self.ub = np.array(bounds[1])
        
        # Random init within bounds
        self.X = self.lb + np.random.rand(n_particles, dimensions) * (self.ub - self.lb)
        self.V = np.zeros_like(self.X) # Initial velocity 0
        
        # Personal Best
        self.P = self.X.copy()
        self.P_best_scores = np.full(n_particles, np.inf)
        
        # Global Best
        self.G = self.X[0].copy()
        self.G_best_score = np.inf

    def snap_to_discrete(self, particle):
        """
        Snap a particle's continuous dimensions to the nearest values in discrete_lists.
        Returns a NEW snapped particle (does not modify the continuous one used for physics).
        """
        if not self.discrete_lists:
            return particle
            
        snapped = particle.copy()
        for idx, standards in self.discrete_lists.items():
            if idx < len(snapped):
                val = snapped[idx]
                # Find nearest standard value
                # Assuming standards is sorted
                # np.searchsorted finds insertion point.
                # But simple absolute difference logic is robust.
                closest = min(standards, key=lambda x: abs(x - val))
                snapped[idx] = closest
        return snapped

    def optimize(self, objective_func, iters, debug=False):
        """
        Run the optimization loop.
        """
        for i in range(iters):
            # 1. Evaluate Particles
            for j in range(self.n_particles):
                # Snap current position to discrete values for evaluation
                # This treats the continuous space as a "Search" space and discrete as "Reality"
                real_position = self.snap_to_discrete(self.X[j])
                
                # Evaluate
                score = objective_func(real_position)
                
                # Update Personal Best
                if score < self.P_best_scores[j]:
                    self.P_best_scores[j] = score
                    self.P[j] = self.X[j].copy() # Store the continuous position that generated good result
                    
                    # Update Global Best
                    if score < self.G_best_score:
                        self.G_best_score = score
                        self.G = self.X[j].copy() # Continuous G
                        if debug:
                            # Print REAL dimensions
                            print(f"[IntelligentPSO] New Global Best at iter {i}: Score={score:.2f}")
                            # print(f"   Real Dims: {real_position}")

            # 2. Update Velocity and Position
            r1 = np.random.rand(self.n_particles, self.dimensions)
            r2 = np.random.rand(self.n_particles, self.dimensions)
            
            # Velocity Update
            # V = w*V + c1*r1*(PersonalBest - Current) + c2*r2*(GlobalBest - Current)
            self.V = self.w * self.V + \
                     self.c1 * r1 * (self.P - self.X) + \
                     self.c2 * r2 * (self.G - self.X)
            
            # Position Update
            self.X = self.X + self.V
            
            # 3. Intelligent Boundary Handling (Clamping)
            # If a particle hits the wall, stop it there.
            # This is better than teleporting because it keeps the particle "looking" at the boundary.
            
            # Check Lower Bounds
            # Check Lower Bounds
            lower_violation = self.X < self.lb
            self.X = np.where(lower_violation, self.lb, self.X)
            self.V[lower_violation] = 0 # Zero velocity at the wall (inelastic collision)
            
            # Check Upper Bounds
            upper_violation = self.X > self.ub
            self.X = np.where(upper_violation, self.ub, self.X)
            self.V[upper_violation] = 0

            # Optional: Convergence Check (if variance is very low)
            
        # Return the best DISCRETE solution
        final_best = self.snap_to_discrete(self.G)
        return self.G_best_score, final_best
