"""Script used for hypothesis testing"""

import numpy as np
from scipy.stats import f, fisher_exact, norm, t


def one_sample_t_test(
    sample_mean,
    sample_size,
    population_mean,
    population_std,
    significance_level,
    test_type,
):
    """Function used to output whether we should accept or reject our hypothesis test for a one sample t-test."""
    if test_type == "two-sided":
        dist_percentile = (1 - significance_level) + (significance_level) / 2
    elif test_type == "left-sided":
        dist_percentile = 1 - significance_level
    elif test_type == "right-sided":
        dist_percentile = 1 - significance_level

    # test statistic
    test_statistic_value = (sample_mean - population_mean) / (population_std**2 / sample_size) ** 0.5

    # find critical values
    if sample_size > 29:
        # normally distributed # CLT
        dist = norm(loc=0, scale=1)
    else:
        degrees_of_freedom = sample_size - 1
        # t test
        dist = t(df=degrees_of_freedom)

    critical_region = dist.ppf(dist_percentile)
    test_statistic_prob = 1 - dist.cdf(abs(test_statistic_value))

    # reject or accept null hypothesis
    if test_type == "two-sided":
        if (test_statistic_value < -1 * critical_region) or (test_statistic_value > critical_region):
            reject_status = "Reject null hypothesis."
        else:
            reject_status = "Insufficient evidence to reject null hypothesis."
    elif test_type == "left-sided":
        if test_statistic_value < -1 * critical_region:
            reject_status = "Reject null hypothesis."
        else:
            reject_status = "Insufficient evidence to reject null hypothesis."
    elif test_type == "right-sided":
        if test_statistic_value > critical_region:
            reject_status = "Reject null hypothesis."
        else:
            reject_status = "Insufficient evidence to reject null hypothesis."

    if test_type == "two-sided":
        p_value = 2 * test_statistic_prob
    else:
        p_value = test_statistic_prob

    return test_statistic_value, critical_region, p_value, reject_status


def two_sample_t_test(
    sample_mean1,
    sample_std1,
    sample_size1,
    sample_mean2,
    sample_std2,
    sample_size2,
    significance_level,
    test_type,
    homogeneity=True,
):
    """Function used to output whether we should accept or reject our hypothesis test for two sample t-test."""
    if test_type == "two-sided":
        dist_percentile = (1 - significance_level) + (significance_level) / 2
    elif test_type == "left-sided":
        dist_percentile = 1 - significance_level
    elif test_type == "right-sided":
        dist_percentile = 1 - significance_level

    # calculate test statistic value
    if homogeneity:
        # assuming variance is the same for both samples
        sample_variance_estimation_numerator = (sample_size1 - 1) * sample_std1**2 + (
            sample_size2 - 1
        ) * sample_std2**2
        sample_variance_estimation_denominator = sample_size1 + sample_size2 - 2
        sample_variance_estimation = sample_variance_estimation_numerator / sample_variance_estimation_denominator

        test_statistic_variance = sample_variance_estimation * (1 / sample_size1 + 1 / sample_size2)

        test_statistic_value = (sample_mean1 - sample_mean2) / test_statistic_variance**0.5
    else:
        # heterogeneity
        # assuming variance is the same for both samples
        # calculate test statistic value
        sample_variance_estimation = sample_std1**2 / sample_size1 + sample_std2**2 / sample_size2

        test_statistic_std = sample_variance_estimation**0.5

        test_statistic_value = (sample_mean1 - sample_mean2) / test_statistic_std

    # critcal region
    if (sample_size1 > 29) and (sample_size2 > 29):
        # CLT
        # normal distribution
        dist = norm(loc=0, scale=1)
    else:
        # t distribution
        degrees_of_freedom = sample_size1 + sample_size2 - 2
        dist = t(df=degrees_of_freedom)

    critical_region = dist.ppf(dist_percentile)
    test_statistic_prob = 1 - dist.cdf(abs(test_statistic_value))

    # reject or accept null hypothesis
    if test_type == "two-sided":
        if (test_statistic_value < -1 * critical_region) or (test_statistic_value > critical_region):
            reject_status = "Reject null hypothesis."
        else:
            reject_status = "Insufficient evidence to reject null hypothesis."
    elif test_type == "left-sided":
        if test_statistic_value < -1 * critical_region:
            reject_status = "Reject null hypothesis."
        else:
            reject_status = "Insufficient evidence to reject null hypothesis."
    elif test_type == "right-sided":
        if test_statistic_value > critical_region:
            reject_status = "Reject null hypothesis."
        else:
            reject_status = "Insufficient evidence to reject null hypothesis."

    # p-values
    if test_type == "two-sided":
        p_value = 2 * test_statistic_prob
    else:
        p_value = test_statistic_prob

    return test_statistic_value, critical_region, p_value, reject_status


def f_test_variance(
    sample_std1,
    sample_size1,
    sample_std2,
    sample_size2,
    significance_level,
    test_type,
):
    """Function used to output whether we should accept or reject our hypothesis test for variance F-test."""
    if test_type == "two-sided":
        dist_percentile = 1 - (significance_level) / 2
    elif test_type == "left-sided":
        dist_percentile = significance_level
    elif test_type == "right-sided":
        dist_percentile = 1 - significance_level

    # calculate test statistic value
    test_statistic_value = sample_std1**2 / sample_std2**2

    # critical region
    # degrees of freedom
    dfn = sample_size1 - 1
    dfd = sample_size2 - 1
    f_dist = f(dfn, dfd)

    if test_type == "two-sided":
        critical_region_right = f_dist.ppf(dist_percentile)
        critical_region_left = f_dist.ppf(1 - dist_percentile)
    else:
        critical_region = f_dist.ppf(dist_percentile)

    # reject or accept null hypothesis
    if test_type == "two-sided":
        if (test_statistic_value < critical_region_left) or (test_statistic_value > critical_region_right):
            reject_status = "Reject null hypothesis."
        else:
            reject_status = "Insufficient evidence to reject null hypothesis."
    elif test_type == "left-sided":
        if test_statistic_value < critical_region:
            reject_status = "Reject null hypothesis."
        else:
            reject_status = "Insufficient evidence to reject null hypothesis."
    elif test_type == "right-sided":
        if test_statistic_value > critical_region:
            reject_status = "Reject null hypothesis."
        else:
            reject_status = "Insufficient evidence to reject null hypothesis."
    return test_statistic_value, critical_region, reject_status


def two_sample_proportion_test(
    sample_size1,
    sample1_counts,
    sample_size2,
    sample2_counts,
    significance_level,
    test_type,
):
    """Function used to output whether we should accept or reject our hypothesis test for
    two_sample_proportion_test."""
    if test_type == "two-sided":
        dist_percentile = 1 - (significance_level) / 2
    elif test_type == "left-sided":
        dist_percentile = significance_level
    elif test_type == "right-sided":
        dist_percentile = 1 - significance_level

    proportion1 = sample1_counts / sample_size1
    proportion2 = sample2_counts / sample_size2
    total_proportion = (sample1_counts + sample2_counts) / (sample_size1 + sample_size2)
    # calculate pooled test statistic value
    test_statistic_value_denom = (
        total_proportion * (1 - total_proportion) * (1 / sample_size1 + 1 / sample_size2)
    ) ** 0.5
    test_statistic_value = (proportion1 - proportion2) / test_statistic_value_denom

    # critcal region
    if (sample_size1 > 29) and (sample_size2 > 29):
        # CLT
        # normal distribution
        dist = norm(loc=0, scale=1)
        critical_region = dist.ppf(dist_percentile)
    else:
        raise Exception("Sample size too small for either sample 1 or two.")

    critical_region = dist.ppf(dist_percentile)
    test_statistic_prob = 1 - dist.cdf(abs(test_statistic_value))

    # reject or accept null hypothesis
    if test_type == "two-sided":
        if (test_statistic_value < -1 * critical_region) or (test_statistic_value > critical_region):
            reject_status = "Reject null hypothesis."
        else:
            reject_status = "Insufficient evidence to reject null hypothesis."
    elif test_type == "left-sided":
        if test_statistic_value < -1 * critical_region:
            reject_status = "Reject null hypothesis."
        else:
            reject_status = "Insufficient evidence to reject null hypothesis."
    elif test_type == "right-sided":
        if test_statistic_value > critical_region:
            reject_status = "Reject null hypothesis."
        else:
            reject_status = "Insufficient evidence to reject null hypothesis."

    # p-values
    if test_type == "two-sided":
        p_value = 2 * test_statistic_prob
    else:
        p_value = test_statistic_prob

    return test_statistic_value, critical_region, p_value, reject_status


def fisher_exact_test(sample_size1, sample1_success, sample_size2, sample2_success, significance_level, test_type):
    """Function used to output whether we should accept or reject our hypothesis test for
    two_sample_proportion_test when the sample size is small ie fisher exact test"""
    if test_type == "two-sided":
        scipy_test_type = "two-sided"
    elif test_type == "left-sided":
        scipy_test_type = "less"
    elif test_type == "right-sided":
        scipy_test_type = "greater"

    sample1_failures = sample_size1 - sample1_success
    sample2_failures = sample_size2 - sample2_success

    # create contingency table
    table = np.array([[sample1_success, sample2_success], [sample1_failures, sample2_failures]])

    # apply fisher exact test
    fisher_exact_result = fisher_exact(table, alternative=scipy_test_type)

    test_statistic_value, p_value = fisher_exact_result

    if p_value < significance_level:
        reject_status = "Reject null hypothesis."
    else:
        reject_status = "Insufficient evidence to reject null hypothesis."

    return test_statistic_value, p_value, reject_status
