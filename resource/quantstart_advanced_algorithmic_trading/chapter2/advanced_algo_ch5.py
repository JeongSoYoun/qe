
# QuantStart
# Advanced Algorithmic Trading 
# Michael L. Halls-Moore, PhD
# Part2 - Chapter 5

import pymc3 as pm
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pymc3.glm import linear

def linear_model(N,beta_0,beta_1,eps_sigma_sq):

    df = pd.DataFrame (

        {
            "x":
                np.random.choice (

                    list(map(lambda x: float(x)/100.0, np.arange(100))),
                    N, # size of choice
                    replace = False # repeition
               )
        }
    )

    eps_mean = 0.0
    df["y"] = beta_0 + beta_1 * df["x"] + np.random.RandomState(42).normal (

        eps_mean,eps_sigma_sq,N
    )

    return df

def glm_mcmc_inference(df, iterations = 5000):


    basic_model = pm.Model()

    with basic_model:

        pm.glm.GLM.from_formula("y~x",df,family = pm.glm.families.Normal())

        start = pm.find_MAP()
        step = pm.NUTS()

        trace = pm.sample(

            iterations,
            step,
            start,
            random_seed = 42,
            progressbar = True
        )

        return trace

if __name__ == "__main__":

    df = linear_model(N = 100, beta_0 = 1.0, beta_1 = 2.0, eps_sigma_sq = 0.5)
    trace = glm_mcmc_inference(df,iterations = 5000)
    sns.lmplot(x="x",y="y",data=df,height=10,fit_reg=False)
    plt.xlim(0.0,1.0)
    plt.ylim(0.0,4.0)

    pm.plot_posterior_predictive_glm(trace,samples=100)
    x = np.linspace(0, 1, 100)
    y = 1.0 + 2.0*x
    plt.plot(x, y, label="True Regression Line", lw=3., c="green") 
    plt.legend(loc=0)
    plt.show()