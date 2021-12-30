
# QuantStart
# Advanced Algorithmic Trading 
# Michael L. Halls-Moore, PhD
# Part 2 - Chapter 4

from fastprogress.fastprogress import ProgressBar
import matplotlib.pyplot as plt
import numpy as np
import pymc3 as pm
import scipy.stats as stats

plt.style.use("ggplot")

def mcmc(alpha,beta,n,z,iterations):

    basic_model = pm.Model()

    with basic_model:

        theta = pm.Beta("theta",alpha=alpha, beta=beta)
        y = pm.Binomial("y",n=n,p=theta,observed=z)
        
        start = pm.find_MAP()
        step = pm.Metropolis()

        trace = pm.sample(

            iterations,step,start,random_seed=1,progressbar=True
        )

        return trace

def plot(x,trace): 

    plt.plot(
        x,
        stats.beta.pdf(x,alpha,beta),
        "--",
        label="Prior",
        color="blue"
    )

    plt.plot(
        x,
        stats.beta.pdf(x,alpha_post,beta_post),
        label="Posterior(Analytic)",
        color="green"
    )

    plt.hist(

        trace["theta"],
        bins=50,
        density=True,
        histtype="step",
        label="Posterior(MCMC)",
        color="red"
    )

    plt.legend(title="Parameters", loc="best")
    plt.show()

if __name__ == "__main__":

    n = 50
    z = 10
    alpha = 12
    beta = 12
    alpha_post = 22
    beta_post = 52
    iterations = 100000

    trace = mcmc(alpha,beta,n,z,iterations)
    x = np.linspace(0,1,100)
    plot(x,trace)