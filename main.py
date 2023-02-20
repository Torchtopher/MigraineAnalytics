import os
import datetime
import seaborn as sns
import calendar
import matplotlib.pyplot as plt
import scipy.stats as stats
import http.client
import pgeocode
import json
from meteostat import Point, Daily
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
import textwrap
import argparse
sns.set_palette("husl")
# paragraph

ZIP_CODE = 28105

class MigraneTimeline:
    

    def __init__(self, name, start_date, end_date, headaches, zip_code) -> None:
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.headaches = headaches
        self.zip_code = zip_code
        self.weather_data = None

    def get_headache_count(self):
        return len(self.headaches)

    """
    :param canvas: reportlab canvas
    :param text: the raw text to wrap
    :param length: the max number of characters per line
    :param x_pos: starting x position
    :param y_pos: starting y position
    :param y_offset: the amount of space to leave between wrapped lines
    """
    def draw_wrapped_line(self, canvas, text, length, x_pos, y_pos, y_offset):
        if len(text) > length:
            wraps = textwrap.wrap(text, length)
            for x in range(len(wraps)):
                canvas.drawCentredString(x_pos, y_pos, wraps[x])
                y_pos -= y_offset
            y_pos += y_offset  # add back offset after last wrapped line
        else:
            canvas.drawCentredString(x_pos, y_pos, text)
        return y_pos

    # uses data from various diffrent funcitions from the migraine timeline class to generate a custom report for the patient
    def generate_report(self):
        LEFT_MARGIN = 60
        # remove old report if it exists
        try:
            os.remove(f"Migrane_report_for_{self.name}.pdf")
        except:
            pass

        # create a pdf file
        pdf = Canvas(f"Migrane_report_for_{self.name}.pdf", pagesize=letter)
        # add logo in top left corner
        # 666 x 531
        # draw image in center of page
        pdf.drawImage("png/logo-color.png", -95, 0, width=800, height=800, preserveAspectRatio=True)    
        # new page
        pdf.showPage()
        # add title
        pdf.setFont("Helvetica-Bold", 28)
        pdf.drawString(LEFT_MARGIN, 720, f"Migrane Report for {self.name}")

        # add date
        pdf.setFont("Helvetica", 12)
        pdf.drawString(LEFT_MARGIN, 690, f"Generated on: {datetime.datetime.now().strftime('%m/%d/%Y')} by Migraine Analytics")
        pdf.drawString(LEFT_MARGIN, 670, f"Total headache count: {self.get_headache_count()}")
        pdf.drawString(LEFT_MARGIN, 650, f"Start date: {self.start_date.strftime('%m/%d/%Y')}")
        pdf.drawString(LEFT_MARGIN, 630, f"End date: {self.end_date.strftime('%m/%d/%Y')}")

        # add purpose of report
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(LEFT_MARGIN, 600, "Purpose and Usage of Report")
        pdf.setFont("Helvetica", 12)
        ''' 
        purpose_string = This report is designed to help both your doctor and you better understand your migraines and how they are affected by various factors.
    The program requires only the dates of when you have headaches and your zip code, but if other data has been tracked it can analyze that.
    The report will show you the following:
        - Graphs of your migraines over time by day, month, and year to find overall trends
        - Statistics about your migraines, such as average number of migraines per month, average number of migraines per year, and the median number of migraines per month
        - Statistically significant correlations between your migraines and other factors, such as weather, and month, and pollen levels
        - If you have tracked other data, such as if certain activites occured or if you took medication, the program will show you the correlation between those factors and your migraines
                - Many people have not tracked this data, so it is not required, but if you have it can help you better understand your migraines and verify if certain factors are causing them
        - General and specific recommendations for how to better manage your migraines
    How to use this report:
        - The report is designed to be used by both you and your doctor, so you can both better understand your migraines and how to manage them.
        - Since patients are not hospialized with migranes, it is has been impossible for doctors to have this data and in a useful format. This report fixes that problem.
    
        # use draw_wrapped_line to wrap the text
        y_pos = 580
        y_offset = 20
        self.draw_wrapped_line(pdf, purpose_string, 80, 250, y_pos, y_offset)
    '''
        pdf.drawString(LEFT_MARGIN, 580, "This report is designed to help both your doctor and you better understand your migraines")
        pdf.drawString(LEFT_MARGIN, 560, "and how they are affected by various factors.")
        pdf.drawString(LEFT_MARGIN, 540, "The program requires only the dates of when you have headaches and your zip code,")
        pdf.drawString(LEFT_MARGIN, 520, "but if other data has been tracked it can analyze that.")
        # set bold and font size
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(LEFT_MARGIN, 480, "The report will show you the following:")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(LEFT_MARGIN, 440, "- Graphs of your migraines over time by day, month, and year to find overall trends")
        pdf.drawString(LEFT_MARGIN, 420, "- Statistics about your migraines, such as average number of migraines per month,")
        pdf.drawString(LEFT_MARGIN, 400, "average number of migraines per year, and the median number of migraines per month")
        pdf.drawString(LEFT_MARGIN, 380, "- Statistically significant correlations between your migraines and other factors,")
        pdf.drawString(LEFT_MARGIN, 360, "such as weather, and month, and pollen levels")
        pdf.drawString(LEFT_MARGIN, 340, "- If you have tracked other data, such as if certain activites occured or if you took")
        pdf.drawString(LEFT_MARGIN, 320, "medication, the program will show you the correlation between those factors and your")
        pdf.drawString(LEFT_MARGIN, 300, "migraines")
        pdf.drawString(LEFT_MARGIN, 280, "- Many people have not tracked this data, so it is not required, but if you have it")
        pdf.drawString(LEFT_MARGIN, 260, "can help you better understand your migraines and verify if certain factors are")
        pdf.drawString(LEFT_MARGIN, 240, "causing them")
        pdf.drawString(LEFT_MARGIN, 220, "- General and specific recommendations for how to better manage your migraines")
        # set bold and title
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(LEFT_MARGIN, 180, "How to use this report:")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(LEFT_MARGIN, 140, "- The report is designed to be used by both you and your doctor, so you can both")
        pdf.drawString(LEFT_MARGIN, 120, "better understand your migraines and how to manage them.")
        pdf.drawString(LEFT_MARGIN, 100, "- Since patients are not hospialized with migranes, it is has been impossible for")
        pdf.drawString(LEFT_MARGIN, 80, "doctors to have this data and in a useful format. This report fixes that problem.")

        # add graphs
        # next page
        pdf.showPage()
        # add title
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(LEFT_MARGIN, 760, "Your Migraines Over Time")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(LEFT_MARGIN, 740, "The following graphs show your migraines over time by day, month, and year.")
        pdf.drawString(LEFT_MARGIN, 720, "These graphs can help you find overall trends in your migraines.")
        # add graphs
        pdf.drawImage("graphs/headaches_per_year.png", 50, 400, width=500, height=300, preserveAspectRatio=True)
        # some explanation
        pdf.drawString(LEFT_MARGIN, 380, "This graph shows the number of migraines you have had each year.")

        most_recent_full_year = self.most_recent_full_year()
        pdf.drawImage(f"graphs/{most_recent_full_year}_headaches_per_month.png", 50, 70, width=500, height=300, preserveAspectRatio=True)
        # some explanation
        pdf.drawString(LEFT_MARGIN, 60, f"This graph shows the number of migraines you have had each month in {most_recent_full_year}, the most recent full year.")
        # next page
        pdf.showPage()
        # add title
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(LEFT_MARGIN, 760, "Your Migraines Over Time, Continued")
        pdf.drawImage("graphs/most_common_day.png", LEFT_MARGIN, 440, width=500, height=300, preserveAspectRatio=True)
        # some explanation
        # set back to normal font
        pdf.setFont("Helvetica", 12)
        pdf.drawString(LEFT_MARGIN, 430, "The red line is the average, which is how many migraines you have on average each day.")
        # the last 6 years of headaches per month in a 3x2 grid of graphs, make them a little smaller so they fit
        true_recent_year = self.end_date.year
        old_left_margin = LEFT_MARGIN
        LEFT_MARGIN = 5
        TOP_Y = 200
        BOTTOM_Y = TOP_Y - 160
        pdf.drawImage(f"graphs/{true_recent_year-5}_headaches_per_month.png", LEFT_MARGIN, TOP_Y, width=200, height=200, preserveAspectRatio=True)
        pdf.drawImage(f"graphs/{true_recent_year-4}_headaches_per_month.png", LEFT_MARGIN+200, TOP_Y, width=200, height=200, preserveAspectRatio=True)
        pdf.drawImage(f"graphs/{true_recent_year-3}_headaches_per_month.png", LEFT_MARGIN+400, TOP_Y, width=200, height=200, preserveAspectRatio=True)
        pdf.drawImage(f"graphs/{true_recent_year-2}_headaches_per_month.png", LEFT_MARGIN, BOTTOM_Y, width=200, height=200, preserveAspectRatio=True)
        pdf.drawImage(f"graphs/{true_recent_year-1}_headaches_per_month.png", LEFT_MARGIN+200, BOTTOM_Y, width=200, height=200, preserveAspectRatio=True)
        pdf.drawImage(f"graphs/{true_recent_year}_headaches_per_month.png", LEFT_MARGIN+400, BOTTOM_Y, width=200, height=200, preserveAspectRatio=True)
        LEFT_MARGIN = old_left_margin
        # some explanation
        pdf.drawString(LEFT_MARGIN, 50, "Per month data of the last 6 years.")
        # next page
        pdf.showPage()
        # add title
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(LEFT_MARGIN, 760, "Migraine Statistics")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(LEFT_MARGIN, 740, "The following is information about what triggers your migraines and what has no effect.")
        pdf.drawString(LEFT_MARGIN, 720, "It will include data like which months are more likely to cause migraines, and if temperature")
        pdf.drawString(LEFT_MARGIN, 700, "or other weather data has an effect.")
        pdf.drawString(LEFT_MARGIN, 680, "If you are interested in the statistical tests used to find this data, please see the appendix.")
        # add title
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(LEFT_MARGIN, 640, "Months")
        pdf.setFont("Helvetica", 12)
        p_value_months = self.boschloo_exact_months()
        months = []
        # loop through dict
        for month, p_value in p_value_months.items():
            if p_value < 0.05:
                months.append(month)
        # if there are no months, then say so
        if len(months) == 0:
            pdf.drawString(LEFT_MARGIN, 620, "There is no month that is more likely to cause migraines.")
        else:
            month_string = '''Based on the data, we can say with very high confidence that during the following months, you are will have a high number of migraines:'''
            pdf.drawString(LEFT_MARGIN, 620, "Based on the data, we can say with very high confidence that during the")
            pdf.drawString(LEFT_MARGIN, 600, "following months, you are will have a high number of migraines:")
            # set font to bold
            pdf.setFont("Helvetica-Bold", 12)
            # add months
            start_x = LEFT_MARGIN
            for month in months:
                pdf.drawString(start_x, 580, month)
                start_x += pdf.stringWidth(month, "Helvetica-Bold", 12) + 10
            pdf.setFont("Helvetica", 12)
            # add some advice
            pdf.drawString(LEFT_MARGIN, 560, "You should look for patterns or triggers during these months, and try to avoid them. Possible triggers")
            pdf.drawString(LEFT_MARGIN, 540, "could be stress from starting school, certain season, or activites during these months.")
        
        # add title
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(LEFT_MARGIN, 500, "Weather")
        pdf.setFont("Helvetica", 12)
        # add some explanation
        pdf.drawString(LEFT_MARGIN, 480, "Next, we will look at the weather data. We will look at the temperature, precipitation and pressure")
        pdf.drawString(LEFT_MARGIN, 460, "to determine if they have an effect on your migraines.")
        # add title
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(LEFT_MARGIN, 420, "Temperature")
        pdf.setFont("Helvetica", 12)
        # get data
        _, p_value_temp, odds_ratio, med_temp, high_percent = self.chi_squared_weather("tavg")
        # convert med_temp to fahrenheit
        med_temp = round(med_temp * 9/5 + 32)
        if p_value_temp < 0.05:
            pdf.drawString(LEFT_MARGIN, 400, "Based on the data, we can say with high confidence that the temperature has an effect on your")
            pdf.drawString(LEFT_MARGIN, 380, f"migraines. The odds of having a migraine on a day with a temperature greater than {med_temp} degrees ")
            pdf.drawString(LEFT_MARGIN, 360, f"is {round((odds_ratio-1)*100, 2)}% more than on a day with a temperature of less than {med_temp} degrees. A total of {round(high_percent*100, 2)}%")
            pdf.drawString(LEFT_MARGIN, 340, f"of your migraines occured on days with a temperature greater than {med_temp} degrees")
        else: 
            pdf.drawString(LEFT_MARGIN, 400, "Based on the data, we can say with high confidence that the temperature does not have an effect on your migraines.")
        # add title
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(LEFT_MARGIN, 300, "Precipitation")
        pdf.setFont("Helvetica", 12)
        # get data
        _, p_value_precip, odds_ratio, med_precip, high_percent = self.chi_squared_weather("prcp")
        if p_value_precip < 0.05:
            pdf.drawString(LEFT_MARGIN, 280, "Based on the data, we can say with confidence that Precipitation has an effect on your migraines.")
            pdf.drawString(LEFT_MARGIN, 260, f"The odds of having a migraine on a day with Precipitation greater than {med_precip} inches is {round((odds_ratio-1)*100, 2)}% more than on a day with Precipitation of less than {med_precip} inches.")
            pdf.drawString(LEFT_MARGIN, 240, f"A total of {round(high_percent*100, 2)}% of your migraines occured on days with precipitation greater than {med_precip} inches.")
        else:
            pdf.drawString(LEFT_MARGIN, 280, "Based on the data, we can say with high confidence that Precipitation does not have an")
            pdf.drawString(LEFT_MARGIN, 260, "effect on your migraines.")
        # add title
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(LEFT_MARGIN, 200, "Barometric Pressure")
        pdf.setFont("Helvetica", 12)
        # get data
        _, p_value_pressure, odds_ratio, med_pressure, high_percent = self.chi_squared_pressure()
        if p_value_pressure < 0.05:
            pdf.drawString(LEFT_MARGIN, 180, "Based on the data, we can say with confidence that pressure has an effect on your migraines.")
            pdf.drawString(LEFT_MARGIN, 160, f"The odds of having a migraine on a day with pressure greater than {med_pressure} inches is {round((odds_ratio-1)*100, 2)}% more than on a day with pressure of less than {med_pressure} inches.")
            pdf.drawString(LEFT_MARGIN, 140, f"A total of {round(high_percent*100, 2)}% of your migraines occured on days with pressure greater than {med_pressure} inches.")
        else:
            pdf.drawString(LEFT_MARGIN, 180, "Based on the data, we can say with high confidence that pressure does not have an")
            pdf.drawString(LEFT_MARGIN, 160, "effect on your migraines.")
        # export to pdf
        pdf.save()


    def most_recent_full_year(self):
        # find most recent full year
        # if the current year has less than 10 months, then the most recent year is the previous year
        if self.end_date.month < 10:
            return self.end_date.year - 1
        else:
            return self.end_date.year


    def pollen_chi_sqared(self, year=None):
        pass

    # find if months have an effect on migraines
    # null hypothesis: there is no correlation between months and migraines
    # can't use chi squared because will have less than 5 values in a cell
    # month should be a number 1-12
    def boschloo_exact_months(self, baseline_month=1):
        all_months = {}
        # initialize dictionary with all months and year combinations, some months will have 0 headaches
        for month in range(1, 13):
            # use start and end date to find all years
            for year in range(self.start_date.year, self.end_date.year + 1):
                if year == self.end_date.year and month > self.end_date.month:
                    break
                all_months[(calendar.month_name[month], year)] = 0
        
        for headache in self.headaches:
            month = headache.month
            month = calendar.month_name[month]
            month = (month, headache.year)
            all_months[month] += 1
        print(all_months)
        # turn months into a list
        all_months_list = list(all_months.values())
        year_avg = {}
        # find average for each year
        for year in range(self.start_date.year, self.end_date.year + 1):
            # sum all months for that year
            sum = 0
            for month in range(1, 13):
                try:
                    sum += all_months[(calendar.month_name[month], year)]
                except KeyError:
                    # if not in dictionary, means it is after the end date
                    continue

            # divide by 12 to get average
            average = sum / 12
            year_avg[year] = average

        print("Average headaches per month: " + str(year_avg))
        # sort and find median
        #all_months_list.sort()
        #median_headaches_per_month = all_months_list[len(all_months_list) // 2]
        #print("Median headaches per month: " + str(median_headaches_per_month))
        
        # for each month, above or below median
        # contingency table, compare each month to january (baseline)
        # month | above media | below median
        # jan           |             |
        # target month | above median | below median
        p_value_lookup = {}
        for month in range(1, 13):
            print("Month: " + calendar.month_name[month])
            # loop through the years and lookup the number of headaches for that month
            # find the number of headaches above and below the average
            target_above_average = 0
            target_below_average = 0
            for year in range(self.start_date.year, self.end_date.year + 1):
                # get the number of headaches for that month
                try:
                    num_headaches = all_months[(calendar.month_name[month], year)]
                except:
                    break # after end date
                if num_headaches >= year_avg[year]:
                    target_above_average += 1
                else:
                    target_below_average += 1
            # find the number of headaches above and below the average for january
            baseline_above_average = 0
            baseline_below_average = 0
            for year in range(self.start_date.year, self.end_date.year + 1):
                # get the number of headaches for that month
                try:
                    num_headaches = all_months[("November", year)]
                except:
                    break # after end date
                if num_headaches > year_avg[year]:
                    baseline_above_average += 1
                else:
                    baseline_below_average += 1
            # contingency table
            # month | above media | below average
            # jan           |             |
            # target month | above average | below average
            #print("Target above average: " + str(target_above_average))
            #print("Target below average: " + str(target_below_average))
            #print("Jan above average: " + str(baseline_above_average))
            #print("Jan below average: " + str(baseline_below_average))
            contingency_table = [[baseline_above_average, baseline_below_average], [target_above_average, target_below_average]]
            # get the boschloo exact test
            res = stats.boschloo_exact(contingency_table)
            if res.pvalue < 0.05:
                print(f"There is a significant correlation between {calendar.month_name[month]} and more migraines")
                print(f"P value {res.pvalue}")
            else:
                print(f"There is no significant correlation between {calendar.month_name[month]} and more migraines")
            
            p_value_lookup[calendar.month_name[month]] = res.pvalue
        return p_value_lookup

    # test if tempature or rain has an effect on migraines
    # null hypothesis: there is no correlation between temperature and migraines
    # field must be one of tavg  tmin  tmax  prcp  snow  wdir  wspd  wpgt pres  tsun
    def chi_squared_pressure(self):
        pressure_delta = 10 # how much pressure must change to be considered a change
        field = "pres"
        # loop through tavg for each day with pandas
        median = self.weather_data.loc[:, field].median()
        print("Total average temperature: " + str(median))        
        # find days without migraines below average temperature
        days_below_average_w_migrane = 0
        days_above_average_w_migrane = 0
        day_below_average_without = 0
        days_above_average_without = 0
        # loop through each day between start and end date
        total_migraines = 0
        previous_pressure = 0
        for day in self.weather_data.iterrows():
            if previous_pressure == 0:
                previous_pressure = day[1][field]
                continue
            print(f"Pressure: {day[1][field]} Previous pressure: {previous_pressure}")
            date = day[0].to_pydatetime()
            # check if there was a migraine that day
            migraine = False
            for headache in self.headaches:
                if headache == date:
                    migraine = True
                    #print("Migraine on " + str(date))
                    total_migraines += 1
                    break
            # check if the temperature was below average
            if abs(day[1][field] - previous_pressure) > pressure_delta:
                if migraine:
                    days_below_average_w_migrane += 1
                else:
                    day_below_average_without += 1
            else:
                if migraine:
                    days_above_average_w_migrane += 1
                else:
                    days_above_average_without += 1
            previous_pressure = day[1][field]
        # find days with migraines below average temperature
        # get the chi squared test
        # make a contingency table
        #                migraine | no migraine
        # below average |         |
        # above average |         |
        # assert all above values are greater than 5
        #assert days_below_average_w_migrane > 5
        #assert days_above_average_w_migrane > 5
        #assert day_below_average_without > 5
        #assert days_above_average_without > 5
        print("Days below average with migraine: " + str(days_below_average_w_migrane))
        print("Days above average with migraine: " + str(days_above_average_w_migrane))
        print("Days below average without migraine: " + str(day_below_average_without))
        print("Days above average without migraine: " + str(days_above_average_without))

        chi2, p, _, _ = stats.chi2_contingency([[days_below_average_w_migrane, day_below_average_without], [days_above_average_w_migrane, days_above_average_without]])
        print(f"chi2 statistic:     {chi2:.5g}")
        print(f"p-value:            {p:.5g}")

        if p < 0.05:
            print(f"There is a significant correlation between {field} and migraines")
            print(f"percent high temp migraine: {days_above_average_w_migrane / total_migraines}")
            print(f"percent low temp migraine: {days_below_average_w_migrane / total_migraines}")
            # calculate odds ratio
            print("Odds ratio: " + str((days_above_average_w_migrane * day_below_average_without) / (days_below_average_w_migrane * days_above_average_without)))
        else:
            print(f"There is no significant correlation between {field} and migraines")
            print("PRESSURE")
        return chi2, p, (days_above_average_w_migrane * day_below_average_without) / (days_below_average_w_migrane * days_above_average_without), median, (days_above_average_w_migrane / total_migraines)




    # test if tempature or rain has an effect on migraines
    # null hypothesis: there is no correlation between temperature and migraines
    # field must be one of tavg  tmin  tmax  prcp  snow  wdir  wspd  wpgt pres  tsun
    def chi_squared_weather(self, field):
        # loop through tavg for each day with pandas
        median = self.weather_data.loc[:, field].median()
        print("Total average temperature: " + str(median))        
        # find days without migraines below average temperature
        days_below_average_w_migrane = 0
        days_above_average_w_migrane = 0
        day_below_average_without = 0
        days_above_average_without = 0
        # loop through each day between start and end date
        total_migraines = 0
        for day in self.weather_data.iterrows():
            date = day[0].to_pydatetime()
            # check if there was a migraine that day
            migraine = False
            for headache in self.headaches:
                if headache == date:
                    migraine = True
                    #print("Migraine on " + str(date))
                    total_migraines += 1
                    break
            # check if the temperature was below average
            if day[1][field] <= median:
                if migraine:
                    days_below_average_w_migrane += 1
                else:
                    day_below_average_without += 1
            else:
                if migraine:
                    days_above_average_w_migrane += 1
                else:
                    days_above_average_without += 1
        # find days with migraines below average temperature
        # get the chi squared test
        # make a contingency table
        #                migraine | no migraine
        # below average |         |
        # above average |         |
        # assert all above values are greater than 5
        assert days_below_average_w_migrane > 5
        assert days_above_average_w_migrane > 5
        assert day_below_average_without > 5
        assert days_above_average_without > 5

        chi2, p, _, _ = stats.chi2_contingency([[days_below_average_w_migrane, day_below_average_without], [days_above_average_w_migrane, days_above_average_without]])
        print(f"chi2 statistic:     {chi2:.5g}")
        print(f"p-value:            {p:.5g}")

        if p < 0.05:
            print(f"There is a significant correlation between {field} and migraines")
            print(f"percent high temp migraine: {days_above_average_w_migrane / total_migraines}")
            print(f"percent low temp migraine: {days_below_average_w_migrane / total_migraines}")
            # calculate odds ratio
            print("Odds ratio: " + str((days_above_average_w_migrane * day_below_average_without) / (days_below_average_w_migrane * days_above_average_without)))
        else:
            print(f"There is no significant correlation between {field} and migraines")
        
        return chi2, p, (days_above_average_w_migrane * day_below_average_without) / (days_below_average_w_migrane * days_above_average_without), median, (days_above_average_w_migrane / total_migraines)

    def graph_per_year(self):
        # create a dictionary with years as keys and headache counts as values
        years = {}
        for headache in self.headaches:
            year = headache.year
            if year not in years:
                years[year] = 0
            years[year] += 1
        # create a list of years and a list of headache counts
        x = list(years.keys())
        y = list(years.values())
        # create a graph
        plot = sns.barplot(x=x, y=y)
        # set the title
        plot.set_title("Headaches per year")
        # set the x and y labels
        plot.set(xlabel="Year", ylabel="Headache count")
        # save the graph
        os.makedirs("graphs", exist_ok=True)
        plot.get_figure().savefig("graphs/headaches_per_year.png")
        return plot
    
    def graph_per_month(self, year):
        print("Graphing headaches per month in " + str(year))
        # create a dictionary with months as keys and headache counts as values
        months = {}
        for headache in self.headaches:
            if headache.year == year:
                month = headache.month
                month = calendar.month_name[month]
                if month not in months:
                    months[month] = 0
                months[month] += 1
        # create a list of months and a list of headache counts
        x = list(months.keys())
        y = list(months.values())
        print(x, y)
        # create a graph
        plot = sns.barplot(x=x, y=y)
        # set the title
        plot.set_title("Headaches per month in " + str(year))
        # set the x and y labels
        plot.set(xlabel="Month", ylabel="Headache count")
        plot.set_xticklabels(plot.get_xticklabels(), rotation=30)
        # save the graph
        os.makedirs("graphs", exist_ok=True)
        plot.get_figure().savefig(f"graphs/{year}_headaches_per_month.png")
        return plot
    
    def graph_all_time_most_common_day(self):
        # get the day of the week for each headache
        days = [headache.weekday() for headache in self.headaches]
        # create a dictionary with days as keys and headache counts as values
        days = {}
        for headache in self.headaches:
            day = headache.weekday()
            if day not in days:
                days[day] = 0
            days[day] += 1
        
        x = []
        y = []
        # create a list of days and a list of headache counts
        # loop over keys and values in dictionary
        for key, value in days.items():
            # convert key to day name
            x.append(key)
        x.sort()
        for day in x:
            y.append(days[day])

        # convert day numbers to day names
        x = [calendar.day_name[day] for day in x]
    
        # create a graph
        plot = sns.barplot(x=x, y=y)
        # set the title
        plot.set_title("All time most common day of the week for headaches")
        # set the x and y labels
        plot.set(xlabel="Day of the week", ylabel="Headache count")
        # add some space between the x and y labels and the graph
        plot.figure.tight_layout()
        # find average headaches per day
        average = sum(y) / len(y)
        # add a horizontal line at the average
        plot.axhline(average, ls="--", color="red")
        # save the graph
        os.makedirs("graphs", exist_ok=True)
        
        plot.get_figure().savefig("graphs/most_common_day.png")
        return plot



# MigraneTimeline class is independent of input type which makes adding support for diffrent data formats much easier
def init_from_iHeadache(filename):
    with open(filename, "r") as f:
        data = f.readlines()
    # strip newlines
    data = [line.strip() for line in data]
    headaches = []
    out = ""
    for line in data:
        # check for name
        if "Patient name : " in line:
            name = line.replace("Patient name : ", "")
        if "Start date: " in line:
            start_date = datetime.datetime.strptime(line.replace("Start date: ", ""), "%m/%d/%Y")
        
        if "Stop date: " in line:
            end_date = datetime.datetime.strptime(line.replace("Stop date: ", ""), "%m/%d/%Y")

        # remove everything after the first space
        line = line.split(" ")[0]
        
        # make sure the line is a valid date
        try:
            date = datetime.datetime.strptime(line, "%m/%d/%Y")
            headaches.append(date)
            out = out + line + "\n"
        except ValueError:
            continue
    with open("iHeadache.txt", "w") as f:
        f.write(out)
    # create timeline
    return MigraneTimeline(name, start_date, end_date, headaches, ZIP_CODE)

def remove_graphs():
    if os.path.exists("graphs"):
        for file in os.listdir("graphs"):
            os.remove(os.path.join("graphs", file))


def load_pollen():
    print("Start data: " + timeline.start_date.strftime("%Y-%m-%d"), "End date: " + timeline.end_date.strftime("%Y-%m-%d"))
    start_date_str = timeline.start_date.strftime("%Y-%m-%d")
    end_date_str = timeline.end_date.strftime("%Y-%m-%d")

    conn = http.client.HTTPSConnection("api.ambeedata.com")
    headers = {
        'x-api-key': "6cbfc0801fee6b0f55cc17f7c6093a3062486a0db9a1318183ef9107bcaedf17",
        'Content-type': "application/json"
        }
    print(f"/history/pollen/by-lat-lng?lat={lat}&lng={lng}from={start_date_str}2012%3A16%3A44&to={end_date_str}%2012%3A16%3A44")
    conn.request("GET", f"/history/pollen/by-lat-lng?lat={lat}&lng={lng}&from={start_date_str}%2012%3A16%3A44&to={end_date_str}%2012%3A16%3A44", headers=headers)
    res = conn.getresponse()
    data = res.read() 

    print(data.decode("utf-8"))
    out = json.loads(data.decode("utf-8"))
    # write to file
    with open("pollen.json", "w") as f:
        json.dump(out, f)



if __name__ == "__main__":  
    # pasre command line arguments
    parser = argparse.ArgumentParser(description="Create graphs from a migraine timeline")
    parser.add_argument("input", help="The input file to use")
    parser.add_argument("zip", help="The zip code to use")
    args = parser.parse_args()
    remove_graphs()
    timeline = init_from_iHeadache("input.txt")

    nomi = pgeocode.Nominatim('us')
    data = nomi.query_postal_code(ZIP_CODE)
    lat = data["latitude"]
    lng = data["longitude"]
    # Set time period
    start = datetime.datetime(timeline.start_date.year, timeline.start_date.month, timeline.start_date.day)
    end = datetime.datetime(timeline.end_date.year, timeline.end_date.month, timeline.end_date.day)

    # Create Point for Vancouver, BC
    location = Point(lat, lng, 70)

    # Get daily data for 2018
    data = Daily(location, start, end)
    data = data.fetch()
    print(data)
    timeline.weather_data = data

    print("Successfully loaded timeline for " + timeline.name)
    print("Headache count: " + str(timeline.get_headache_count()))
    
    timeline.graph_all_time_most_common_day()
    plt.clf()
    timeline.graph_per_year()
    plt.clf()
    print("Start date: " + timeline.start_date.strftime("%Y-%m-%d"), "End date: " + timeline.end_date.strftime("%Y-%m-%d"))
    for year in range(timeline.start_date.year, timeline.end_date.year + 1):
        print(year)
        plot = timeline.graph_per_month(year)
        plt.clf()
    
    timeline.chi_squared_weather("tavg")
    timeline.chi_squared_weather("prcp")
    timeline.chi_squared_weather("wspd")
    timeline.boschloo_exact_months(baseline_month=1)
    timeline.generate_report()