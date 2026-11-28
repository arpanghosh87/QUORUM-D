"""Focused mathematical checks for the paper, not an evaluation SDK."""
import numpy as np
from itertools import combinations


def exchangeable_moments(probabilities):
    """Distribution of K correct votes; conditional on K choose uniformly."""
    q=np.asarray(probabilities,dtype=float)
    if q.ndim!=1 or len(q)<4 or len(q)%2!=0 or not np.isfinite(q).all() or (q<0).any() or not np.isclose(q.sum(),1,atol=1e-12,rtol=0):
        raise ValueError("probabilities for an odd panel of at least three required")
    q=q/q.sum()
    n=len(q)-1;k=np.arange(n+1)
    p=float(k@q/n)
    if not 0<p<1: raise ValueError("nonconstant margins required")
    joint=float((k*(k-1))@q/(n*(n-1)))
    rho=(joint-p*p)/(p*(1-p))
    variance=float(((k-k@q)**2)@q)
    if variance==0: raise ValueError("zero count variance has no finite ESS")
    return dict(p=p,rho=rho,ess=float(n*n*p*(1-p)/variance),majority=float(q[k>n/2].sum()))


def covariance_variance(weights,covariance,reference_variance):
    """Variance of weighted mean and explicitly reference-normalized size."""
    w=np.asarray(weights,float); s=np.asarray(covariance,float)
    if w.ndim!=1 or not w.size or not np.isfinite(w).all() or (w<0).any() or not np.isfinite(w.sum()) or w.sum()<=0 or s.shape!=(len(w),len(w)) or not np.isfinite(s).all() or not np.allclose(s,s.T,atol=1e-12,rtol=0) or np.linalg.eigvalsh(s).min() < -1e-12 or not np.isfinite(reference_variance) or reference_variance<=0:
        raise ValueError("invalid covariance or weights")
    w=w/w.sum();v=float(w@s@w)
    if v<=0: raise ValueError("positive variance required")
    return v,reference_variance/v


def constrained_weights(covariance):
    """Exact active-face enumeration for small positive definite panels only."""
    s=np.asarray(covariance,float)
    if s.ndim!=2 or s.shape[0]!=s.shape[1] or not 1<=len(s)<=12 or not np.isfinite(s).all() or not np.allclose(s,s.T,atol=1e-12,rtol=0) or np.linalg.eigvalsh(s).min()<=1e-10:
        raise ValueError("positive definite small panel required")
    best=None
    for k in range(1,len(s)+1):
        for idx in combinations(range(len(s)),k):
            a=np.linalg.solve(s[np.ix_(idx,idx)],np.ones(k));a/=a.sum()
            if (a < -1e-12).any(): continue
            w=np.zeros(len(s));w[list(idx)]=np.maximum(a,0);w/=w.sum()
            v=float(w@s@w)
            if best is None or v<best[0]: best=(v,w)
    return best[1]


def conditional_errors(errors,mask):
    """Observed complete-case error correlation on a routed subset."""
    e=np.asarray(errors); m=np.asarray(mask)
    if e.ndim!=2 or e.shape[1]<2 or m.shape!=(len(e),) or m.dtype!=bool or not np.isin(e,[0,1]).all():
        raise ValueError("binary errors and boolean mask required")
    x=e[m];n=len(x)
    if n<2: return dict(n=n,rates=None,correlation=None)
    v=np.cov(x,rowvar=False);d=np.sqrt(np.outer(v.diagonal(),v.diagonal()))
    r=np.divide(v,d,out=np.full_like(v,np.nan),where=d>0)
    return dict(n=n,rates=x.mean(0).tolist(),correlation=[[float(y) if np.isfinite(y) else None for y in row] for row in r])


def paired_bootstrap(a,b,seed=2026,reps=2000,clusters=None):
    """Percentile interval for mean paired difference; cluster resample if supplied."""
    a=np.asarray(a,float);b=np.asarray(b,float)
    if a.ndim!=1 or a.shape!=b.shape or len(a)<2 or not np.isfinite(a).all() or not np.isfinite(b).all() or not isinstance(reps,int) or reps<100:
        raise ValueError("aligned finite pairs and at least 100 replicates required")
    d=a-b
    if clusters is None: groups=np.arange(len(d))
    else:
        groups=np.asarray(clusters)
        if groups.shape!=d.shape: raise ValueError("aligned cluster IDs required")
    _,idx=np.unique(groups,return_inverse=True)
    sums=np.bincount(idx,weights=d);counts=np.bincount(idx)
    if len(sums)<2: raise ValueError("at least two resampling units required")
    rng=np.random.default_rng(seed)
    draws=np.empty(reps)
    for i in range(reps):
        j=rng.integers(len(sums),size=len(sums));draws[i]=sums[j].sum()/counts[j].sum()
    return dict(mean=float(d.mean()),lower=float(np.quantile(draws,.025)),upper=float(np.quantile(draws,.975)),units=len(sums),reps=reps)
