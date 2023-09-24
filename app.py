from flask import Flask, render_template, request, jsonify  # Import jsonify


app = Flask(__name__)


import pandas as pd

# Sample data (replace with your actual data)
data = {
    'A': [270, 279.3, 320, 365, 334, 335, 369, 497.3, 525],
    'B': [288.6, 301, 316.6, 339.6, 351.6, 377, 397, 534, 597.6],
    'C': [281, 291.6, 335, 374.3, 388.3, 414.3, 391.3, 552.6, 613.3],
    'D': [279.6, 291, 322.3, 353, 358.6, 356.6, 399.3, 551.3, 567],
    'E': [279.6, 295.3, 339, 379, 373.6, 404.3, 442.6, 607, 667.6],
    'F': [342.6, 360.6, 408, 481, 493.3, 537.3, 506, 771.6, 845]
}

# Create a DataFrame
df = pd.DataFrame(data, index=['week 0', 'week 1', 'week 2', 'week 3', 'week 4', 'week 5', 'week 6', 'week 7', 'week 8'])

def predict_weights(feed_type, initial_weight):
    # Ensure that feed_type is valid (you can add more validation as needed)
        # Calculate the pattern for the selected feed type
        # Calculate the pattern for the selected feed type
    initial_weight_week0 = df.at['week 0', feed_type]
    pattern = []
    for week in range(1, 9):
        weight_week = df.at[f'week {week}', feed_type]
        pattern_value = weight_week / initial_weight_week0
        pattern.append(pattern_value)

	# Predict the weights for the next 8 we
    # Use the calculated pattern to predict the weights for weeks 1 to 8
    predicted_weights = [initial_weight * pattern_value for pattern_value in pattern]

    return predicted_weights

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        feed_type = request.form['feed_type']
        initial_weight = float(request.form['initial_weight'])

        # Perform prediction
        predictions = predict_weights(feed_type, initial_weight)

        if predictions is None:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"error": "Invalid feed type or data not available."})
            else:
                return "Invalid feed type or data not available."

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({"predictions": predictions})
        else:
            pass
    return render_template('index.html', feed_type=None, initial_weight=None, predictions=None)

if __name__ == '__main__':
    app.run(debug=True)

