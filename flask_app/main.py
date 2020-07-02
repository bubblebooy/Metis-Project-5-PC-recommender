import time
from flask import Flask, request, render_template, jsonify, make_response
from make_prediction import get_build_details, get_build_list, get_recommendations, price_mask, cluster_plot

# create a flask object
app = Flask(__name__)


# creates an association between the / page and the entry_page function (defaults to GET)
@app.route('/')
def entry_page():
    build_list = get_build_list()

    params = {"plot_type" : 'svd',
                "c" : "k_predict"}
    return render_template('index.html', build_list = build_list, params = params, recommendations = None)

# creates an association between the /predict_recipe page and the render_message function
# (includes POST requests which allow users to enter in data via form)
@app.route('/build/', methods=['GET', 'POST'])
# @app.route('/b/<build>')
def render_message(build = None):
    build_list = get_build_list()
    selected_builds = request.cookies.get('selected_builds')
    if selected_builds is None or selected_builds == '':
        selected_builds = []
    else:
        selected_builds=selected_builds.split(',')
    print(selected_builds)

    params = {"threshold" : 0.5,
                "state" : "Mexico City"}

    for key, val in request.form.items():
        if key == 'build':
            build = val
            params[key] = val
            if not build in selected_builds:
                selected_builds.append(build)
        elif key == 'remove_build':
            if val == 'reset':
                selected_builds = [build]
            if val in selected_builds:
                selected_builds.remove(val)
            if build == val:
                if selected_builds:
                    build = selected_builds[-1]
                    params['build'] = build
                else:
                    build = None
                    params['build'] = ""
        else:
            params[key] = val
    if params.get('multi') != 'true':
        selected_builds = [build]

    # show user final message
    build_details = None
    recommendations = None

    if build is not None:
        recommendations = get_recommendations(selected_builds, svd = params.get('svd'))
        build_details = get_build_details(build)
    if recommendations is not None:
        if selected_builds:
            recommendations = recommendations[~recommendations.isin(selected_builds)]

        print("test")
        if params['min_price'] and recommendations is not None:
            recommendations = price_mask(recommendations, min = float(params['min_price']))
        if params['max_price'] and recommendations is not None:
            recommendations = price_mask(recommendations, max = float(params['max_price']))

    cluster_plot(build = selected_builds, recommendations = recommendations, plot_type = params.get('plot_type'), c = params.get('c'))
    random_number = time.time()

    # "Logistic Regression: rate: {0:.3f} --- mortality rate: {1:.3f}".format(results[0],results[1])
    # list(zip(["survival rate","mortality rate"],mortality(features_vals)))
    resp = make_response(render_template('index.html', message = build_details, recommendations = recommendations, build_list = build_list, params = params, selected_builds = selected_builds, random_number=random_number))
    resp.set_cookie('selected_builds',','.join(selected_builds))
    return resp

if __name__ == '__main__':
    app.run(debug=True)
