from flask import Flask, render_template, request, send_from_directory, url_for
import os

from app.restcountries import get_country_data, plot_population_pie, plot_area_bar
from app.weather import get_weather_data, plot_clustered_comparison, save_weather_csv
from app.news import get_news_data, plot_news_by_source, save_news_csv
from app.exchange import get_exchange_data, plot_exchange_bar, save_exchange_csv
from app.covid import get_covid_data, plot_covid_graph, save_covid_csv


def create_app(app: Flask):
    export_dir = os.path.join(app.root_path, "exports")
    os.makedirs(export_dir, exist_ok=True)

    @app.route("/")
    def home():
        return render_template("index.html", current_path=request.path)

    @app.route("/restcountries", methods=["GET", "POST"])
    def restcountries():
        countries_list = []
        successful_countries = []
        population_chart = None
        area_chart = None

        if request.method == "POST":
            country_names = [request.form.get(f"country_name_{i}") for i in range(5)]
            for name in country_names:
                if not name or not name.strip():
                    continue
                data = get_country_data(name.strip())
                countries_list.append(data)
                if "error" not in data:
                    successful_countries.append(data)

            if successful_countries:
                population_chart = plot_population_pie(successful_countries)
                area_chart = plot_area_bar(successful_countries)

        return render_template(
            "restcountries.html",
            countries_list=countries_list,
            population_chart=population_chart,
            area_chart=area_chart,
            current_path=request.path,
            download_countries_csv_url="/download/restcountries/csv",
        )

    @app.route("/download/restcountries/csv")
    def download_restcountries_csv():
        return send_from_directory(export_dir, "restcountries_data.csv", as_attachment=True)

    @app.route("/news", methods=["GET", "POST"])
    def news_view():
        news_data = []
        news_by_source = None
        csv_download_url = None

        q = ""
        from_date = ""
        to_date = ""
        language = ""
        sort_by = "publishedAt"
        page_size = 80

        if request.method == "POST":
            q = (request.form.get("q") or "").strip()
            from_date = (request.form.get("from_date") or "").strip()
            to_date = (request.form.get("to_date") or "").strip()
            language = (request.form.get("language") or "").strip()
            sort_by = (request.form.get("sort_by") or "publishedAt").strip()

            try:
                page_size = int(request.form.get("page_size") or 80)
            except ValueError:
                page_size = 80
            page_size = max(1, min(100, page_size))

            res = get_news_data(
                q=q,
                from_date=from_date or None,
                to_date=to_date or None,
                sort_by=sort_by,
                language=language or None,
                page_size=page_size,
                page=1,
            )

            if "error" in res:
                news_data = [{"error": res["error"]}]
            else:
                news_data = res.get("articles", [])
                if news_data:
                    news_by_source = plot_news_by_source(news_data)
                    csv_path = os.path.join(export_dir, "news_data.csv")
                    save_result = save_news_csv(news_data, csv_path)
                    if "error" not in save_result:
                        csv_download_url = "/download/news/csv"

        return render_template(
            "news.html",
            news_data=news_data,
            news_by_source=news_by_source,
            csv_download_url=csv_download_url,
            current_path=request.path,
            q=q,
            from_date=from_date,
            to_date=to_date,
            language=language,
            sort_by=sort_by,
            page_size=page_size,
        )

    @app.route("/download/news/csv")
    def download_news_csv():
        return send_from_directory(export_dir, "news_data.csv", as_attachment=True)

    @app.route("/exchange", methods=["GET", "POST"])
    def exchange():
        base = "USD"
        symbols = ""
        exchange_data = None
        chart_b64 = None
        csv_download_url = None
        error = None

        if request.method == "POST":
            base = (request.form.get("base") or "USD").upper()
            symbols = (request.form.get("symbols") or "").upper().replace(" ", "")

            resp = get_exchange_data(base=base, symbols=symbols or None)
            if isinstance(resp, dict) and resp.get("error"):
                error = resp.get("error")
            else:
                rows = resp
                exchange_data = rows
                if rows:
                    chart_b64 = plot_exchange_bar(rows)
                    csv_name = "exchange_snapshot.csv"
                    csv_path = os.path.join(export_dir, csv_name)
                    csv_res = save_exchange_csv(rows, csv_path)
                    if csv_res.get("error"):
                        error = csv_res.get("error")
                    else:
                        csv_download_url = url_for("download_exchange_csv")

        return render_template(
            "exchange.html",
            current_path=request.path,
            base=base,
            symbols=symbols,
            exchange_data=exchange_data,
            chart_b64=chart_b64,
            csv_download_url=csv_download_url,
            error=error,
        )

    @app.route("/download/exchange/csv")
    def download_exchange_csv():
        return send_from_directory(export_dir, "exchange_snapshot.csv", as_attachment=True)

    @app.route("/covid", methods=["GET"])
    def covid():
        error = None
        records = []
        chart_b64 = None
        csv_download_url = None

        data = get_covid_data()
        if isinstance(data, dict) and data.get("error"):
            error = data.get("error")
        else:
            records = data or []
            if records:
                chart_b64 = plot_covid_graph(records)
                csv_filename = "covid_global_history.csv"
                csv_path = os.path.join(export_dir, csv_filename)
                save_result = save_covid_csv(records, csv_path)
                if not save_result.get("error"):
                    csv_download_url = url_for("download_covid_csv")

        return render_template(
            "covid.html",
            records=records,
            chart_b64=chart_b64,
            csv_download_url=csv_download_url,
            error=error,
            current_path=request.path,
        )

    @app.route("/download/covid/csv")
    def download_covid_csv():
        return send_from_directory(export_dir, "covid_global_history.csv", as_attachment=True)


    @app.route("/weather", methods=["GET", "POST"])
    def weather():
        locations = []
        weather_data = []
        comparison_chart = None
        csv_download_url = None
        error_msg = None
        units = "metric"
        lang = ""

        if request.method == "POST":
            units = (request.form.get("units") or "metric").strip()
            lang = (request.form.get("lang") or "").strip() or None

            raw_locations = []
            for i in range(1, 4):
                name = (request.form.get(f"loc{i}_name") or "").strip()
                lat = (request.form.get(f"loc{i}_lat") or "").strip()
                lon = (request.form.get(f"loc{i}_lon") or "").strip()
                if lat and lon:
                    raw_locations.append({
                        "display_name": name or f"Location {i}",
                        "lat": lat,
                        "lon": lon,
                    })

            if not raw_locations:
                error_msg = "Please enter at least one location with latitude and longitude."
            else:
                for loc in raw_locations:
                    res = get_weather_data(
                        lat=loc["lat"],
                        lon=loc["lon"],
                        units=units,
                        lang=lang,
                        display_name=loc["display_name"],
                    )
                    if isinstance(res, dict) and res.get("error"):
                        error_msg = (error_msg or "") + f" {loc['display_name']}: {res['error']}"
                    else:
                        weather_data.append(res)

                if weather_data:
                    comparison_chart = plot_clustered_comparison(weather_data)
                    csv_path = os.path.join(export_dir, "weather_data.csv")
                    save_res = save_weather_csv(weather_data, csv_path)
                    if save_res.get("ok"):
                        csv_download_url = url_for("download_weather_csv")
                    else:
                        error_msg = save_res.get("error", error_msg)

            locations = raw_locations

        return render_template(
            "weather.html",
            current_path=request.path,
            locations=locations,
            weather_data=weather_data,
            comparison_chart=comparison_chart,
            csv_download_url=csv_download_url,
            error_msg=error_msg,
            units=units,
            lang=lang or "",
        )
    @app.route("/download/weather/csv")
    def download_weather_csv():
        return send_from_directory(export_dir, "weather_data.csv", as_attachment=True)

    return app
