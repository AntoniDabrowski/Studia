import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, cauchy

plt.style.use('seaborn-whitegrid')


def confidence_interval_for_mu_known_sigma(random_sample_1, random_sample_2, sigma_1, sigma_2, alpha):
    mean_1 = np.mean(random_sample_1)
    mean_2 = np.mean(random_sample_2)
    n_1 = random_sample_1.shape[0]
    n_2 = random_sample_2.shape[0]
    assert n_1 == n_2
    sigma = np.sqrt(np.power(sigma_1, 2) / n_1 + np.power(sigma_2, 2) / n_2)
    z_alpha_half = norm.ppf(1 - alpha/2)

    lower_bound = (mean_1 - mean_2) - z_alpha_half * sigma
    upper_bound = (mean_1 - mean_2) + z_alpha_half * sigma
    return lower_bound, upper_bound, upper_bound - lower_bound


def plt_sample(random_sample, title):
    plt.hist(random_sample)
    plt.title(title)
    plt.show()


def plt3_confidence_intervals(title, mus_1, mus_2, sigmas_1, sigmas_2, random_sample_gen_num, n, alpha, total_size=50):
    fig, axs = plt.subplots(4, 1, figsize=(10, 5))
    fig.suptitle(title)
    for plot_num, (mu_1, sigma_1, mu_2, sigma_2) in enumerate(zip(mus_1, sigmas_1, mus_2, sigmas_2)):
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
            if random_sample_gen_num == 1:
                random_sample_gen = np.random.normal
            elif random_sample_gen_num == 2:
                random_sample_gen = np.random.logistic
            elif random_sample_gen_num == 3:
                random_sample_gen = cauchy.rvs
            while True:
                random_sample_1 = random_sample_gen(mu_1, sigma_1, n)
                random_sample_2 = random_sample_gen(mu_2, sigma_2, n)
                mean_1 = np.mean(random_sample_1)
                mean_2 = np.mean(random_sample_2)
                if np.abs(mean_1) < 10 and np.abs(mean_2) < 10:
                    break

            mean = mean_1 - mean_2
            mu = mu_1 - mu_2
            lower_bound, upper_bound, size = confidence_interval_for_mu_known_sigma(random_sample_1, random_sample_2,
                                                                                    sigma_1, sigma_2, alpha)
            l.append(lower_bound)
            u.append(upper_bound)
            s.append(size)
            if lower_bound <= mu <= upper_bound:
                if i < 100:
                    l_good.append(mean - lower_bound)
                    u_good.append(upper_bound - mean)
                    y_good.append(mean)
                    x_good.append(i)
                counter += 1
            else:
                if i < 100:
                    l_bad.append(mean - lower_bound)
                    u_bad.append(upper_bound - mean)
                    y_bad.append(mean)
                    x_bad.append(i)
        interv_good = np.array([l_good, u_good])
        interv_bad = np.array([l_bad, u_bad])
        axs[plot_num].errorbar(x_good, y_good, yerr=interv_good, fmt='.k')
        axs[plot_num].errorbar(x_bad, y_bad, yerr=interv_bad, fmt='.r')
        axs[plot_num].plot(np.arange(100), np.ones(total_size) * mu, c='g')
        axs[plot_num].set_xticks([])
        axs[plot_num].set_xlabel('mu_1=' + str(mu_1) + ", sigma_1=" + str(sigma_1) + ', mu_2=' + str(mu_2) + \
                                 ", sigma_2=" + str(sigma_2) + ", error rate=" + \
                                 str((1 - (counter / total_size)) * 100)[:5] + \
                                 "%, confidence interval = [" + str(np.median(l))[:5] + ", " + str(np.median(u))[:5] + \
                                 "], confidence interval length = " + str(np.median(size))[:5])
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    alpha = 0.05
    n = 10000
    total_size = 1000
    # (a)
    mus_1 = [0,0,0,0]
    mus_2 = [0,1,0,1]
    sigma_1 = [1,1,1,1]
    sigma_2 = [1,1,2,2]
    plt3_confidence_intervals("Normal distribution", mus_1, mus_2, sigma_1, sigma_2, 1, n, alpha, total_size=total_size)
    # (b)
    plt3_confidence_intervals("Logistic distribution", mus_1, mus_2, sigma_1, sigma_2, 2, n, alpha, total_size=total_size)
    # (c)
    plt3_confidence_intervals("Cauchy distribution", mus_1, mus_2, sigma_1, sigma_2, 3, n, alpha, total_size=total_size)
