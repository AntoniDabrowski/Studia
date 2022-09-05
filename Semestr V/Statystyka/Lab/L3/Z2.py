import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, cauchy

plt.style.use('seaborn-whitegrid')


def confidence_interval_for_mu_known_sigma(random_sample, sigma, alpha):
    mean = np.mean(random_sample)
    n = random_sample.shape[0]
    z_alpha_half = norm.ppf(1 - alpha / 2)
    lower_bound = mean - z_alpha_half * sigma / np.sqrt(n)
    upper_bound = mean + z_alpha_half * sigma / np.sqrt(n)
    return lower_bound, upper_bound, upper_bound - lower_bound


def confidence_interval(random_sample, alpha):
    mean = np.mean(random_sample)
    n = random_sample.shape[0]
    sigma = np.sqrt(np.sum(np.power(random_sample - mean, 2) / (n - 1)))
    z_alpha_half = norm.ppf(1 - alpha)
    lower_bound = mean - z_alpha_half * sigma / np.sqrt(n)
    upper_bound = mean + z_alpha_half * sigma / np.sqrt(n)
    return lower_bound, upper_bound, upper_bound - lower_bound


def plt_sample(random_sample, title):
    plt.hist(random_sample)
    plt.title(title)
    plt.show()


def plt_confidence_intervals(title, mu, sigma, random_sample_gen, alpha, total_size=50):
    l_good = []
    u_good = []
    y_good = []
    x_good = []
    l_bad = []
    u_bad = []
    y_bad = []
    x_bad = []
    counter = 0
    for i in range(total_size):
        random_sample = random_sample_gen()
        mean = np.mean(random_sample)
        lower_bound, upper_bound, size = confidence_interval_for_mu_known_sigma(random_sample, sigma, alpha)
        # print(lower_bound,mu,upper_bound)
        if lower_bound <= mu <= upper_bound:
            l_good.append(mean - lower_bound)
            u_good.append(upper_bound - mean)
            y_good.append(mean)
            x_good.append(i)
            counter += 1
        else:
            l_bad.append(mean - lower_bound)
            u_bad.append(upper_bound - mean)
            y_bad.append(mean)
            x_bad.append(i)
    interv_good = np.array([l_good, u_good])
    interv_bad = np.array([l_bad, u_bad])
    plt.errorbar(x_good, y_good, yerr=interv_good, fmt='.k')
    plt.errorbar(x_bad, y_bad, yerr=interv_bad, fmt='.r')
    plt.plot(np.arange(total_size), np.ones(total_size) * mu, c='g')
    plt.title(title)
    print(str((counter / total_size) * 100) + "%")
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
            mean = np.mean(random_sample)
            lower_bound, upper_bound, size = confidence_interval_for_mu_known_sigma(random_sample, sigma, alpha)
            l.append(lower_bound)
            u.append(upper_bound)
            s.append(size)
            if lower_bound <= mu <= upper_bound:
                if i % 10 == 0:
                    l_good.append(mean - lower_bound)
                    u_good.append(upper_bound - mean)
                    y_good.append(mean)
                    x_good.append(i)
                counter += 1
            else:
                if i % 10 == 0:
                    l_bad.append(mean - lower_bound)
                    u_bad.append(upper_bound - mean)
                    y_bad.append(mean)
                    x_bad.append(i)
        interv_good = np.array([l_good, u_good])
        interv_bad = np.array([l_bad, u_bad])
        axs[plot_num].errorbar(x_good, y_good, yerr=interv_good, fmt='.k')
        axs[plot_num].errorbar(x_bad, y_bad, yerr=interv_bad, fmt='.r')
        axs[plot_num].plot(np.arange(total_size), np.ones(total_size) * mu, c='g')
        axs[plot_num].set_xticks([])
        axs[plot_num].set_xlabel('mu=' + str(mu) + ", sigma=" + str(sigma) + ", error rate=" + \
                str((1 - (counter / total_size)) * 100)[:5] + "%, confidence interval = [" + str(np.median(l))[:5] + \
                                 ", " + str(np.median(u))[:5] + "], confidence interval length = "+str(np.median(size))[:5])
        print(len(x_good),len(x_bad))
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
            lower_bound, upper_bound, size = confidence_interval_for_mu_known_sigma(random_sample, sigma, alpha)
            l.append(lower_bound)
            u.append(upper_bound)
            s.append(size)
            if lower_bound <= mu <= upper_bound:
                if i % 100 == 0:
                    l_good.append(mean - lower_bound)
                    u_good.append(upper_bound - mean)
                    y_good.append(mean)
                    x_good.append(i)
                counter += 1
            else:
                if i % 100 == 0:
                    l_bad.append(mean - lower_bound)
                    u_bad.append(upper_bound - mean)
                    y_bad.append(mean)
                    x_bad.append(i)
        interv_good = np.array([l_good, u_good])
        interv_bad = np.array([l_bad, u_bad])
        axs[plot_num].errorbar(x_good, y_good, yerr=interv_good, fmt='.k')
        axs[plot_num].errorbar(x_bad, y_bad, yerr=interv_bad, fmt='.r')
        axs[plot_num].plot(np.arange(total_size), np.ones(total_size) * mu, c='g')
        axs[plot_num].set_xticks([])
        axs[plot_num].set_xlabel(parameter_name + '=' + str(mu)[:5] + ", error rate=" + str((1 - (counter / total_size)) \
                                    * 100)[:5] + "%, confidence interval=[" + str(np.median(l))[:5] + ", " + \
                                    str(np.median(u))[:5] + "], confidence interval length = "+str(np.median(size))[:5])
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    alpha = 0.05
    n = 1000
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
