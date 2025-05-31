import numpy as np

def pso(func, lb, ub, ieqcons=[], f_ieqcons=None, args=(), kwargs={},
        swarmsize=600, omega=0.5, phip=0.5, phig=0.5, maxiter=1000,
        minstep=1e-8, minfunc=1e-8, debug=False):
    assert len(lb) == len(ub)
    lb = np.array(lb)
    ub = np.array(ub)
    vhigh = np.abs(ub - lb)
    vlow = -vhigh

    obj = lambda x: func(x, *args, **kwargs)
    if f_ieqcons is None:
        cons = (lambda x: np.array([0])) if not len(ieqcons) \
            else (lambda x: np.array([y(x, *args, **kwargs) for y in ieqcons]))
    else:
        cons = lambda x: np.array(f_ieqcons(x, *args, **kwargs))

    def is_feasible(x, eps=1e-12):
        cons_val = cons(x)
        print(f'Constraint values: {cons_val}')
        return np.all(cons_val >= -eps)  # strictly >=0; small epsilon for numeric tolerance

    # Helper: generate a feasible position
    def random_feasible_point():
        for _ in range(10000):
            candidate = lb + np.random.rand(len(lb)) * (ub - lb)
            if is_feasible(candidate):
                return candidate
        raise RuntimeError("Cannot find feasible initial particle!")

    # Initialize
    S, D = swarmsize, len(lb)
    x = np.zeros((S, D))
    v = np.zeros_like(x)
    p = np.zeros_like(x)
    fp = np.full(S, np.inf)
    g = None
    fg = np.inf

    # Feasible initialization
    for i in range(S):
        x[i, :] = random_feasible_point()
        p[i, :] = x[i, :].copy()
        fp[i] = obj(p[i, :])
        if i == 0 or (fp[i] < fg and is_feasible(p[i, :])):
            g = p[i, :].copy()
            fg = fp[i]
        v[i, :] = vlow + np.random.rand(D) * (vhigh - vlow)

    # Main loop
    it = 1
    while it <= maxiter:
        rp = np.random.uniform(size=(S, D))
        rg = np.random.uniform(size=(S, D))
        for i in range(S):
            v[i, :] = omega * v[i, :] + phip * rp[i, :] * (p[i, :] - x[i, :]) + phig * rg[i, :] * (g - x[i, :])
            x[i, :] = x[i, :] + v[i, :]

            # Project to bounds
            x[i, :] = np.clip(x[i, :], lb, ub)

            # Ensure feasibility
            if not is_feasible(x[i, :]):
                # Option 1: resample until feasible
                x[i, :] = random_feasible_point()
                # Option 2 (alternative): reflect or repair (optional)

            fx = obj(x[i, :])

            # Personal best update
            if is_feasible(x[i, :]) and (fx < fp[i] or not is_feasible(p[i, :])):
                p[i, :] = x[i, :].copy()
                fp[i] = fx

                # Global best update
                if fx < fg or not is_feasible(g):
                    if debug:
                        print(f'New best for swarm at iteration {it}: {x[i, :]} {fx}')
                    tmp = x[i, :].copy()
                    stepsize = np.sqrt(np.sum((g - tmp) ** 2)) if g is not None else np.inf
                    if np.abs(fg - fx) <= minfunc:
                        print(f'Stopping search: Swarm best objective change less than {minfunc}')
                        return tmp, fx
                    elif stepsize <= minstep:
                        print(f'Stopping search: Swarm best position change less than {minstep}')
                        return tmp, fx
                    else:
                        g = tmp.copy()
                        fg = fx
        if debug:
            print(f'Best after iteration {it}: {g} {fg}')
        it += 1

    print(f'Stopping search: maximum iterations reached --> {maxiter}')
    if not is_feasible(g):
        print("However, the optimization couldn't find a feasible design. Sorry")
    return g, fg
