.PHONY: all scrape scrape-async eda visualize clean

all: scrape eda visualize

scrape:
	cd CodeAlpha_WebScraping && python scrape_books.py --out ../CodeAlpha_EDA/CodeAlpha_EDA/books.csv
	cp CodeAlpha_EDA/CodeAlpha_EDA/books.csv CodeAlpha_DataVisualization/books.csv

scrape-async:
	cd CodeAlpha_WebScraping && python scrape_books_async.py --out ../CodeAlpha_EDA/CodeAlpha_EDA/books.csv
	cp CodeAlpha_EDA/CodeAlpha_EDA/books.csv CodeAlpha_DataVisualization/books.csv

eda:
	cd CodeAlpha_EDA/CodeAlpha_EDA && python eda_analysis.py --input books.csv --outdir eda_outputs

visualize:
	cd CodeAlpha_DataVisualization && python visualize.py --input books.csv --outdir dashboard

clean:
	rm -f CodeAlpha_EDA/CodeAlpha_EDA/books.csv
	rm -f CodeAlpha_DataVisualization/books.csv
	rm -rf CodeAlpha_EDA/CodeAlpha_EDA/eda_outputs
	rm -rf CodeAlpha_DataVisualization/dashboard
