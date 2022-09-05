import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, cauchy
from scipy.stats import chi2

plt.style.use('seaborn-whitegrid')


def confidence_interval_for_sigma_known_mu(random_sample, mu, alpha):
    n = random_sample.shape[0]
    sigma = np.sum(np.power(random_sample - mu, 2)) / (n - 1)
    chi2_right = chi2.ppf(alpha / 2, n - 1)
    chi2_left = chi2.ppf(1 - alpha / 2, n - 1)
    lower_bound = sigma*(n-1) / chi2_left
    upper_bound = sigma*(n-1) / chi2_right
    return lower_bound, upper_bound, upper_bound - lower_bound



def plt_sample(random_sample, title):
    plt.hist(random_sample)
    plt.title(title)
    plt.show()



def plt3_confidence_intervals(title, mus, sigmas, random_sample_gens, alpha, total_size=50):
    fig, axs = plt.subplots(3, 1, figsize=(10, 5))
    fig.suptitle(title)
    for plot_num, (random_sample_gen, mu, sigma) in enumerate(zip(random_sample_gens, mus, sigmas)):
        l_good = []
        u_good = []
        y_good = []
        x_good = []
        l_bad = []
        u_bad = []
        y_bad = []
        x_bad = []
        counter = 0
        l = []
        u = []
        s = []
        for i in range(total_size):
            random_sample = random_sample_gen()
            lower_bound, upper_bound, size = confidence_interval_for_sigma_known_mu(random_sample, mu, alpha)
            n = random_sample.shape[0]
            sample_sigma = np.sum(np.power(random_sample - mu, 2)) / (n - 1)
            l.append(lower_bound)
            u.append(upper_bound)
            s.append(size)
            if lower_bound <= np.power(sigma,2) <= upper_bound:
                if i % 100 == 0:
                    l_good.append(sample_sigma - lower_bound)
                    u_good.append(upper_bound - sample_sigma)
                    y_good.append(sample_sigma)
                    x_good.append(i)
                counter += 1
            else:
                if i % 100 == 0:
                    l_bad.append(sample_sigma - lower_bound)
                    u_bad.append(upper_bound - sample_sigma)
                    y_bad.append(sample_sigma)
                    x_bad.append(i)
        interv_good = np.array([l_good, u_good])
        interv_bad = np.array([l_bad, u_bad])
        axs[plot_num].errorbar(x_good, y_good, yerr=interv_good, fmt='.k')
        axs[plot_num].errorbar(x_bad, y_bad, yerr=interv_bad, fmt='.r')
        axs[plot_num].plot(np.arange(total_size), np.ones(total_size) * np.power(sigma,2), c='g')
        axs[plot_num].set_xticks([])
        axs[plot_num].set_xlabel('mu=' + str(mu) + ", sigma^2=" + str(np.power(sigma,2)) + ", error rate=" + \
                str((1 - (counter / total_size)) * 100)[:5] + "%, confidence interval = [" + str(np.median(l))[:5] + \
                                 ", " + str(np.median(u))[:5] + "], confidence interval length = "+ \
                                 str(np.median(u)-np.median(l))[:5])
    fig.tight_layout()
    plt.show()


def plt3_confidence_intervals_single(title, mus, sigmas, random_sample_gens, alpha, parameter_name, total_size=50):
    fig, axs = plt.subplots(3, 1, figsize=(10, 5))
    fig.suptitle(title)
    for plot_num, (random_sample_gen, mu, sigma) in enumerate(zip(random_sample_gens, mus, sigmas)):
        l_good = []
        u_good = []
        y_good = []
        x_good = []
        l_bad = []
        u_bad = []
        y_bad = []
        x_bad = []
        counter = 0
        l = []
        u = []
        s = []
        for i in range(total_size):
            random_sample = random_sample_gen()
            mean = np.mean(random_sample)
            lower_bound, upper_bound, size = confidence_interval_for_sigma_known_mu(random_sample, mu, alpha)
            n = random_sample.shape[0]
            sample_sigma = np.sqrt(np.sum(np.power(random_sample - mean, 2) / (n - 1)))
            l.append(lower_bound)
            u.append(upper_bound)
            s.append(size)
            if lower_bound <= np.power(sigma,2) <= upper_bound:
                if i % 100 == 0:
                    l_good.append(sample_sigma - lower_bound)
                    u_good.append(upper_bound - sample_sigma)
                    y_good.append(sample_sigma)
                    x_good.append(i)
                counter += 1
            else:
                if i % 100 == 0:
                    l_bad.append(sample_sigma - lower_bound)
                    u_bad.append(upper_bound - sample_sigma)
                    y_bad.append(sample_sigma)
                    x_bad.append(i)
        interv_good = np.array([l_good, u_good])
        interv_bad = np.array([l_bad, u_bad])
        axs[plot_num].errorbar(x_good, y_good, yerr=interv_good, fmt='.k')
        axs[plot_num].errorbar(x_bad, y_bad, yerr=interv_bad, fmt='.r')
        axs[plot_num].plot(np.arange(total_size), np.ones(total_size) * np.power(sigma,2), c='g')
        axs[plot_num].set_xticks([])
        axs[plot_num].set_xlabel("variance = " + str(np.power(sigma,2))[:5] + ", error rate=" + str((1 - (counter / total_size)) \
                                    * 100)[:5] + "%, confidence interval=[" + str(np.median(l))[:5] + ", " + \
                                    str(np.median(u))[:5] + "], confidence interval length = "+ \
                                    str(np.median(u)-np.median(l))[:5])
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    alpha = 0.05
    n = 100
    total_size = 1000
    # (a)
    # mu = 0
    # sigma = 1
    # random_sample = np.random.normal(mu, sigma, n)
    # plt_sample(random_sample, "Normal distribution")
    plt3_confidence_intervals("Normal distribution", [0, 0, 0], [1, 2, 3],
                              [lambda: np.random.normal(0, 1, n), lambda: np.random.normal(0, 2, n),
                               lambda: np.random.normal(0, 3, n)], alpha, total_size=total_size)
    # (b)
    # mu = 0
    # sigma = 1
    # random_sample = np.random.logistic(mu, sigma, n)
    # plt_sample(random_sample, "Logistic distribution")
    plt3_confidence_intervals("Logistic distribution", [0, 0, 0], [1, 2, 3],
                              [lambda: np.random.logistic(0, 1, n), lambda: np.random.logistic(0, 2, n),
                               lambda: np.random.logistic(0, 3, n)], alpha, total_size=total_size)
    # (c)
    # mu = 0
    # sigma = 1
    # random_sample = cauchy.rvs(loc=mu, scale=sigma, size=n)
    # plt_sample(random_sample, "Cauchy distribution")
    plt3_confidence_intervals("Cauchy distribution", [0, 0, 0], [1, 2, 3],
                              [lambda: cauchy.rvs(loc=0, scale=1, size=n),
                               lambda: cauchy.rvs(loc=0, scale=2, size=n),
                               lambda: cauchy.rvs(loc=0, scale=3, size=n)], alpha, total_size=total_size)
    # (d)
    # lam = 1
    # random_sample = np.random.exponential(lam, n)
    # plt_sample(random_sample, "Exponential distribution")
    plt3_confidence_intervals_single("Exponential distribution", [1, 1 / 2, 1 / 3],
                                     [np.power(1, 2), np.power(1 / 2, 2), np.power(1 / 3, 2)],
                                     [lambda: np.random.exponential(1, n), lambda: np.random.exponential(1 / 2, n),
                                      lambda: np.random.exponential(1 / 3, n)], alpha, "lambda", total_size=total_size)
    # (e)
    # v = 1
    # random_sample = np.random.chisquare(v, n)
    # plt_sample(random_sample, "Chi-square distribution")
    plt3_confidence_intervals_single("Chi-square distribution", [1, 2, 3], [2, 4, 6],
                                     [lambda: np.random.chisquare(1, n), lambda: np.random.chisquare(2, n),
                                      lambda: np.random.chisquare(3, n)], alpha, "v", total_size=total_size)
