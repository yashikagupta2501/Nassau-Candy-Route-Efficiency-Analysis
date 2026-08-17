# Nassau Candy Route Efficiency Analysis
## Business & Logistics Performance Report

---

## 1. Executive Summary

This project analyzes shipment, route, product, factory, region, state, and shipping-mode data for Nassau Candy Distributor.

The objective is to identify operational bottlenecks, high-risk routes, shipment delay patterns, and their potential business impact.

The analysis was performed using Python, Pandas, NumPy, Matplotlib, and Jupyter Notebook.

---

## 2. Dataset Overview

- Total Records: 10,194
- Columns: 22
- Valid Records: 9,009
- Invalid Lead-Time Records: 1,185
- Delayed Shipments: 2,147
- Overall Delay Rate: 23.83%
- Average Lead Time: 466.28 days
- Median Lead Time: 365 days
- Total Sales: 141,783.63
- Total Gross Profit: 93,442.80
- Total Units: 38,654
- Unique Factories: 5
- Unique Routes: 196
- Unique States: 59
---

## 3. Key Findings

### Factory Analysis

Secret Factory recorded the highest factory-level delay rate at approximately 26.67%.

Sugar Shack recorded a delay rate of approximately 25.81%, while Wicked Choccy's and Lot's O' Nuts recorded approximately 24.39% and 23.38% respectively.

The Other Factory recorded the lowest delay rate at approximately 19.51%.

---

### Region Analysis

The Interior region recorded the highest regional delay rate at approximately 24.15%.

Pacific recorded approximately 23.92%, Atlantic approximately 23.61%, and Gulf approximately 23.60%.

The relatively similar delay rates across regions indicate that delays are not restricted to a single geographic region.

---

### Shipping Mode Analysis

Standard Class had the highest delay rate at approximately 33.68%.

Second Class recorded a delay rate of approximately 15.20%.

Same Day and First Class shipments recorded zero delayed shipments in the analyzed dataset.

This suggests that Standard Class shipments should receive particular attention for service-level improvement.

---

### Product Analysis

Product-level analysis shows differences in shipment delay rates across products.

Nerds recorded the highest delay rate among the analyzed products, at approximately 66.67%.

Everlasting Gobstopper recorded a delay rate of approximately 33.33%, followed by SweeTARTS at approximately 30.00%.

Lickable Wallpaper recorded approximately 27.85%, while Wonka Gum recorded approximately 25.51%.

Among the high-volume Wonka Bar products, Wonka Bar - Milk Chocolate recorded 1,884 shipments and 469 delayed shipments, resulting in a delay rate of approximately 24.89%.

Wonka Bar - Triple Dazzle Caramel recorded 1,790 shipments and 427 delayed shipments, resulting in a delay rate of approximately 23.85%.

These results indicate that product-level delay rates vary considerably. However, products with very low shipment volumes should be interpreted carefully, while high-volume products should be monitored because delays can affect a larger number of shipments.

---

### High-Risk Route Analysis

Several routes showed elevated delay rates.

The highest-risk routes included:

- Sugar Shack → New Jersey
- Wicked Choccy's → South Dakota
- Wicked Choccy's → West Virginia
- Sugar Shack → Connecticut
- Secret Factory → New Hampshire
- Secret Factory → Quebec
- Lot's O' Nuts → South Dakota
- Wicked Choccy's → British Columbia
- Wicked Choccy's → New Mexico
- The Other Factory → New York

Several routes recorded a 100% delay rate. However, some of these routes had very low shipment volumes, such as one or two shipments. Therefore, these routes should be treated as high-risk indicators rather than definitive evidence of consistently poor route performance.

Lot's O' Nuts → South Dakota recorded a delay rate of approximately 85.71%.

Wicked Choccy's → British Columbia recorded approximately 66.67%.

Wicked Choccy's → New Mexico recorded approximately 64.71%.

The Other Factory → New York recorded approximately 63.64%.

These routes should be prioritized for further investigation while considering shipment volume alongside delay rate.

---

## 4. Route Volume vs Lead Time

The correlation between route shipment volume and average lead time was approximately -0.001.

This indicates an almost negligible linear relationship between shipment volume and average lead time.

Therefore, shipment volume alone does not appear to explain differences in average lead time across routes.

---

## 5. Business Impact

The analysis shows that delayed shipments represent a significant operational issue.

Out of 9,009 valid shipments, 2,147 shipments were classified as delayed, resulting in an overall delay rate of 23.83%.

The dataset represents:

- Total Sales: 141,783.63
- Total Gross Profit: 93,442.80
- Total Units: 38,654

Because delayed shipments affect a substantial portion of valid shipments, improving route and delivery performance can have an important operational and business impact.

Further analysis of delayed versus non-delayed sales, units, and gross profit can be used to quantify the financial impact of shipment delays more precisely.

---

## 6. Recommendations

Based on the analysis, the following actions are recommended:

1. Prioritize investigation of high-risk routes while considering both delay rate and shipment volume.
2. Review Standard Class shipment processes because of its 33.68% delay rate.
3. Monitor high-volume products with significant numbers of delayed shipments.
4. Investigate factory-level operational differences, particularly at higher-delay facilities.
5. Analyze transportation and fulfillment processes for routes with unusually long lead times.
6. Use route-level KPIs to continuously monitor delay rate and lead-time performance.
7. Develop a dashboard for tracking shipment volume, delays, sales, and route performance.

---

## 7. Tools Used

- Python
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook

---

## 8. Conclusion

The analysis identifies important operational bottlenecks across factories, shipping modes, products, regions, and routes.

The overall delay rate among valid shipments was 23.83%, with Standard Class showing the highest shipping-mode delay rate at 33.68%.

Factory-level analysis showed the highest delay rate at Secret Factory at 26.67%, while the Interior region recorded the highest regional delay rate at 24.15%.

Several routes also showed high delay rates, although some high-risk routes had very low shipment volumes.

Overall, route-level monitoring, targeted investigation of high-risk routes, and improvements in Standard Class shipment processes can help reduce delays and improve logistics efficiency.

---

## 9. Project Outputs

The project includes visualizations for:

- Factory-wise shipment delay rate
- Region-wise shipment delay rate
- Ship-mode-wise shipment delay rate
- Top products by delay rate
- Top high-risk routes by delay rate

These visualizations are available in the `outputs` folder.