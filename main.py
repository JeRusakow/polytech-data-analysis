import pandas as pd
import matplotlib.pyplot as plt
import json
import seaborn as sns
import argparse
import os
from os import path
from datetime import datetime


start_time = datetime.utcnow()
# parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument("path", metavar="p", help="Path to dataset files")
parser.add_argument("output_path", metavar="o", help="Path to save data")
args = parser.parse_args()
path_to_dataset = args.path

path_to_save_data = args.output_path
if not path.exists(path_to_save_data):
    os.mkdir(path_to_save_data)

death_data_full = pd.read_csv(f"{path_to_dataset}/2015_data.csv", usecols=["sex", "age_recode_27", "education_2003_revision", "month_of_death", "day_of_week_of_death", "358_cause_recode"])
print(f"Read {len(death_data_full)} rows of data for year 2015")

# print(f"Columns: {len(death_data_full.columns)}\n{death_data_full.columns}")

with open(f"{path_to_dataset}/2015_codes.json", "r") as json_codes:
    codes = json.load(json_codes)

# male vs female death rates
men_died = len(death_data_full[death_data_full.sex == "M"])
women_died = len(death_data_full[death_data_full.sex == "F"])
print(f"Men died: {men_died}\nWomen died: {women_died}")


fig1, ax1 = plt.subplots( dpi=200)

slices = [men_died, women_died]
labels = ["Men", "Woman"]

ax1.pie(slices, labels=labels, startangle=90, autopct='%1.1f%%')
ax1.set_title("Men and women death ratio")
# plt.show()
plt.savefig(f"{path_to_save_data}/men_vs_women.png")
print("'Men and women death ratio' chart saved")


# age of death, men and women
data = death_data_full[["sex", "age_recode_27"]]
data = data[data.age_recode_27 != 27]
male_deaths = data[data.sex == "M"].groupby("age_recode_27").count().reset_index("age_recode_27")
female_deaths = data[data.sex == "F"].groupby("age_recode_27").count().reset_index("age_recode_27")

codes_age = {int(key): val.replace(" years", "") for key, val in codes["age_recode_27"].items()}
codes_age[1] = "Under 1 month"
codes_age[2] = "1 - 11 months"

male_deaths.replace(codes_age, inplace=True)
female_deaths.replace(codes_age, inplace=True)

fig1, ax1 = plt.subplots(dpi=200, figsize=(10, 5))
plt.xticks(rotation=80)
ax1.bar(x=male_deaths.age_recode_27, height=male_deaths.sex, alpha=0.5, label="Men")
ax1.bar(x=female_deaths.age_recode_27, height=female_deaths.sex, alpha=0.5, label="Women")
ax1.grid()
ax1.legend()
ax1.set_title("Death by age in men and women")

plt.savefig(f"{path_to_save_data}/deaths_by_age.png")
print("'Death by age in men and women' chart saved")


# age of death by education

codes_education = {int(key): val for key, val in codes["education_2003_revision"].items()}

death_age_by_education = death_data_full[["age_recode_27", "education_2003_revision"]]
death_age_by_education = death_age_by_education[death_age_by_education.age_recode_27 != 27]
death_age_by_education = death_age_by_education.groupby(["education_2003_revision", "age_recode_27"]).size().unstack("education_2003_revision").fillna(0)
death_age_by_education = death_age_by_education.div(death_age_by_education.sum(axis=1), axis=0)
death_age_by_education.columns = [codes_education[idx] for idx in death_age_by_education.columns]
death_age_by_education.index = [codes_age[idx] for idx in death_age_by_education.index]

death_age_by_education

fig1, ax1 = plt.subplots(dpi=200, figsize=(10,5))

death_age_by_education.plot(kind="bar", stacked=True, ax=ax1, legend=True, title="Death ratio by education")

#plt.show()
plt.savefig(f"{path_to_save_data}/age_of_death_by_education.png")
print("'Death ratio by education' chart saved")


# death by day of week
codes_day_of_week = {int(key): val for key, val in codes["day_of_week_of_death"].items()}

death_by_day_of_week = death_data_full[["day_of_week_of_death", "age_recode_27"]]
death_by_day_of_week = death_by_day_of_week[(death_by_day_of_week.age_recode_27 != 27) & (death_by_day_of_week.day_of_week_of_death != 9)]
death_by_day_of_week = death_by_day_of_week.groupby(["day_of_week_of_death", "age_recode_27"]).size().unstack("day_of_week_of_death").fillna(0)

overall_deaths_by_age = death_by_day_of_week.sum(axis=1)
overall_deaths_by_age.index = [codes_age[idx] for idx in overall_deaths_by_age.index]

death_by_day_of_week = death_by_day_of_week.div(death_by_day_of_week.sum(axis=1), axis=0)
death_by_day_of_week.columns = [codes_day_of_week[idx] for idx in death_by_day_of_week.columns]
death_by_day_of_week.index = [codes_age[idx] for idx in death_by_day_of_week.index]

mean_probability = death_by_day_of_week.mean()
expected_probability = 1 / 7.

death_by_day_of_week -= expected_probability
death_by_day_of_week /= expected_probability


fig1, ax1 = plt.subplots(dpi=200, figsize=(5,5))
sns.heatmap(death_by_day_of_week, ax=ax1)
ax1.set_title("Death probability by the day of week")

#plt.show()
plt.savefig(f"{path_to_save_data}/death_by_day_of_week.png")
print("'Death probability by the day of week' chart saved")


# death by month
codes_month = {int(key): val for key, val in codes["month_of_death"].items()}

death_by_month = death_data_full[["month_of_death", "age_recode_27"]]
death_by_month = death_by_month[death_by_month.age_recode_27 != 27]
death_by_month = death_by_month.groupby(["month_of_death", "age_recode_27"]).size().unstack("month_of_death").fillna(0)

death_by_month = death_by_month.div(death_by_month.sum(axis=1), axis=0)
death_by_month.columns = [codes_month[idx] for idx in death_by_month.columns]
death_by_month.index = [codes_age[idx] for idx in death_by_month.index]

mean_probability = death_by_month.mean()
expected_probability = 1 / 12.

death_by_month -= expected_probability
death_by_month /= expected_probability


fig1, ax1 = plt.subplots(dpi=200, figsize=(5,5))
sns.heatmap(death_by_month, ax=ax1)
ax1.set_title("Death probability by month")

#plt.show()
plt.savefig(f"{path_to_save_data}/death_by_month.png")
print("'Death probability by month' chart saved")


# the most common death causes
codes_death_causes = {int(key): val for key, val in codes["358_cause_recode"].items()}

death_commonest_causes = death_data_full[["358_cause_recode"]].groupby("358_cause_recode").size().to_frame().reset_index("358_cause_recode")
death_commonest_causes.columns = ["358_cause_recode", "count"]
death_commonest_causes.sort_values(by="count", inplace=True, ascending=False)
death_commonest_causes.replace({"358_cause_recode": codes_death_causes}, inplace=True)

death_commonest_causes["idx"] = range(len(death_commonest_causes))


fig1, ax1 = plt.subplots(dpi=200, figsize=(7,3.5))
ax1.hist(death_commonest_causes[["count"]], bins=len(death_commonest_causes), density=True, cumulative=True)
ax1.grid()
ax1.set_title("Death causes chart")

#plt.show()
plt.savefig(f"{path_to_save_data}/death_causes_hist.png")
print("'Death causes hist' chart saved")

#
# TEMPORAL TRENDS
#
#
# disposition of corpses trends
years = range(2005, 2016)
fields_of_interest = ["method_of_disposition", "manner_of_death"]

metadata = {}
years = range(2005, 2016)

for year in years:
    data = pd.read_csv(f"{path_to_dataset}/{year}_data.csv", usecols=fields_of_interest)
    metadata[year] = {field: data[[field]].groupby(field).size() for field in fields_of_interest}

for year in years:
    for field in fields_of_interest:
        metadata[year][field] = {
            key: (val / sum(metadata[year][field]))
            for key, val in metadata[year][field].items()
        }

fig, ax = plt.subplots(dpi=200)
ax.plot(years, [metadata[year]["method_of_disposition"]["B"] for year in years], label="Burial")
ax.plot(years, [metadata[year]["method_of_disposition"]["C"] for year in years], label="Cremation")
ax.plot(years, [metadata[year]["method_of_disposition"]["U"] for year in years], label="Unknown")
ax.plot(years, [metadata[year]["method_of_disposition"]["O"] for year in years], label="Other")
ax.grid()
ax.set_xlim([2005, 2015])
ax.set_ylim([-0.001, None])
ax.set_xticks(years)
ax.legend()
ax.set_title("Bodies disposition trends")

#plt.show()
plt.savefig(f"{path_to_save_data}/disposition_methods.png")

# Manner of death
manner_of_death_codes = {int(key) if key.isnumeric() else key: val for key, val in codes["manner_of_death"].items()}

for year_data in metadata.values():
    year_data["manner_of_death"] = {manner_of_death_codes[key]: val for key, val in year_data["manner_of_death"].items()}

fig, ax = plt.subplots(dpi=200)
for manner_of_death in manner_of_death_codes.values():
    if manner_of_death == "Natural": break
    data = [
        metadata[year]["manner_of_death"][manner_of_death]
        if manner_of_death in metadata[year]["manner_of_death"] else 0.
        for year in years
    ]
    ax.plot(years, data, label=manner_of_death)
# ax.set_yscale("log")
ax.grid()
ax.legend()
ax.set_title("Manner of death ratio over years")
ax.set_xlim([min(years), max(years)])
ax.set_xticks(years)
ax.set_ylim([-0.001, None])

#plt.show()
plt.savefig(f"{path_to_save_data}/Manner of death ratio.png")
print("'Manner of death ratio' chart saved")

end_time = datetime.utcnow()
print(f"\nTame taken for running python: {end_time - start_time}")
