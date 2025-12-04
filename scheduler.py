import math
import random

def get_bin(ci_old, cur_CI, CIs):
    min_ci = min(CIs)
    max_ci = max(CIs)

    # For 6 bins
    bin_width = (max_ci - min_ci) / 5

    if ci_old >= max_ci:
        old = 5 
    elif ci_old <= min_ci:
        old =  0
    else:
        old = int((ci_old - min_ci) / bin_width + 1)

    if cur_CI >= max_ci:
        new = 5 
    elif cur_CI <= min_ci:
        new =  0
    else:
        new = int((cur_CI - min_ci) / bin_width + 1)

    return old, new

def get_execution_probability(bin_old, bin_new, recent_CIs, time_remaining_hours):
    benefit = bin_old - bin_new
    
    # No benefit = no execution
    if benefit <= 0:
        return 0.0

    # Base probability: logarithmic growth
    base_prob = 0.1 * math.log(benefit + 1)

    # Hard boost at high benefit
    if benefit >= 4:
        base_prob = 1.0
    if benefit == 3:
        base_prob = .5

    urgency_factor = 1
    # Urgency: strongly increases as deadline approaches
    if time_remaining_hours < 4:
        # Clamp: guaranteed finish before deadline
        base_prob = 1
    else:
        urgency_factor = 3 / (1 + math.log(time_remaining_hours + 1))

    # Detect CI trend
    ci_trend = recent_CIs[-2] - recent_CIs[-1]

    # CI dropping 
    if ci_trend > 1:  # CI dropping
        if benefit < 4:
            return 0.001   

    # CI rising, act more aggressively
    elif ci_trend < 1 and benefit >= 1:
        urgency_factor *= 10

    final_prob = min(1.0, base_prob * urgency_factor)
    return final_prob


# def scheduler(job_id, cur_CI, CI_at_schedule, now, expirationDate, CIs_last_3_before_now, logs):
#     delta = expirationDate - now
#     remaining_hours = delta.total_seconds() / 3600

#     if now > expirationDate:
#         logs[job_id] = ("late", cur_CI, CI_at_schedule, now, CI_at_schedule - cur_CI)
#         return
    
#     bin_old, bin_new = get_bin(CI_at_schedule, cur_CI, CIs_last_3_before_now)
    
#     # Always execute at low CI
#     if bin_new == 0 or bin_new == 1:
#         logs[job_id] = ("executed at low CI", cur_CI, CI_at_schedule, now, CI_at_schedule - cur_CI)
#         return

#     prob = get_execution_probability(bin_old, bin_new, CIs_last_3_before_now, remaining_hours)
#     if random.random() < prob:
#         logs[job_id] = ("executed", cur_CI, CI_at_schedule, now, CI_at_schedule - cur_CI)


def scheduler(job_id, cur_CI, CI_at_schedule, now, expirationDate, CIs_last_3_before_now, logs):
    delta = expirationDate - now
    remaining_hours = delta.total_seconds() / 3600

    bin_old, bin_new = get_bin(CI_at_schedule, cur_CI, CIs_last_3_before_now)
    
    if now >= expirationDate:
        logs[job_id] = ("executed_late", cur_CI, CI_at_schedule, now, CI_at_schedule - cur_CI)
    elif bin_new < 1:# or bin_new == 1: 
        logs[job_id] = ("executed_low_CI", cur_CI, CI_at_schedule, now, CI_at_schedule - cur_CI)
    else:
        prob = get_execution_probability(bin_old, bin_new, CIs_last_3_before_now, remaining_hours)
        r = random.random()
        if r < prob:
            logs[job_id] = ("executed_benefit", cur_CI, CI_at_schedule, now, CI_at_schedule - cur_CI)


# def scheduler(job_id, cur_CI, CI_at_schedule, now, expirationDate, CIs_last_3_before_now, logs):
    
#     if now >= expirationDate:
#         logs[job_id] = ("late", cur_CI, CI_at_schedule, now, CI_at_schedule - cur_CI)
#     else:
#         p = random.random()
#         r = random.random()
#         if r < p:
#             logs[job_id] = ("executed", cur_CI, CI_at_schedule, now, CI_at_schedule - cur_CI)