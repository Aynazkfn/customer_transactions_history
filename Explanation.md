### Explanation 
The project can be summerized into 3 main phases. I explained each phase below:

### EDA
In the EDA four main goals are achieved:
- Create an ordered (descending) plot that shows the total number of transactions per customer from the most active customer to the least active one.
- Given any product ID, create a plot to show its transaction frequency per month for the year 2018.
- Given any Customer_id, check the seasonality effect in this data set.
- At any time, list the top 5 products that drove the highest sales over the last six months.
to make the interactive plots, I used plotly. the analysis done for one customer and one material. The complete analysis is available in the dashboard.

### Model
Since I observed the seasonality, and a general decreasing trend for most of the materials, Seasonal Autoregressive Integrated Moving Average (SARIMA) model is a good choice to predict the the monthly sales to each customer. 
- I developed a time-series prediction using SARIMA to predict the sales for the duration of Jan-2019 to Mar-2020 to one supplier.
- I saved the model and upload the file called "finalized-model".
- I created a separate file to load the saved model and evaluat the results.
- I used Root Mean Squared Error as a performance metric to measure the performance of the model.
- Later I developed a LSTM model to predict the sales to the same customer for the same period for the comparison purpose, since LSTM has the ability to learn cycles or seasonal behavior in the trend
- I concluded that for some points in the trend the LSTM model performs better, and for some other points, the SARIMA model performs better, But the general performance of two model was quite the same.

### Dashboard
The dashboard consists in two main tabs:
- In the first tab, we visualized the monthly sales amount for the year for every combinaion of customer-product-year.
- In the second tab, the results of the sales prediction for to each customer in the duration of Jan-2019 to Mar-2020 in visualized in comparison with the actual sales.
- Ready assets are used to design the general outlook of the dashboard.


