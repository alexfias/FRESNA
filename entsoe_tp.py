from entsoe import EntsoePandasClient
import pandas as pd
import matplotlib.pyplot as plt


def calc_generation_per_unit(country_code, start, psr_type=None, periods=365):
	client = EntsoePandasClient(api_key="f92c4029-439b-4e67-ab0d-0906353966eb")



	ts = pd.DataFrame()

	for day in pd.date_range(start, periods=periods):
		print(day)
		end = start+pd.Timedelta(days=1)
		ts = pd.concat([ts,client.query_generation_per_plant(country_code, day, day+pd.Timedelta(days=1),psr_type)])
	ts.to_csv('generation_per_unit_'+str(psr_type)+'_'+str(country_code)+'.csv')

	return ts

def calc_generation_per_country(country_code, start, psr_type=None,periods=365):
	client = EntsoePandasClient(api_key="f92c4029-439b-4e67-ab0d-0906353966eb")
	ts_country = pd.DataFrame()

	for day in pd.date_range(start, periods=periods):
		print(day)
		end = start+pd.Timedelta(days=1)
		ts_country = pd.concat([ts_country,client.query_generation(country_code, day, day+pd.Timedelta(days=1),psr_type)])
	ts_country.to_csv('generation'+str(psr_type)+'_'+str(country_code)+'.csv')

	return ts_country


start = pd.Timestamp('20170101 00:00:00')
country_code = 'ES' #country code
psr_type = ['B05'] #power plant type
periods = 365
ts = calc_generation_per_unit(country_code, start, psr_type,periods)

ts_country = calc_generation_per_country(country_code, start, psr_type,periods)

print(ts_country)
ts_sum = pd.DataFrame(ts.sum(axis=1),columns=['Fossil Hard coal'])
print(ts_sum)
plt.plot(ts_country-ts_sum)
plt.title('Country - aggregated power plants-'+str(country_code)+'-'+str(psr_type))
plt.xlabel('hour of year')
plt.ylabel('Production difference [MW]')
plt.tight_layout()
plt.savefig('production_difference_'+str(country_code)+'-'+str(psr_type)+'.pdf')
