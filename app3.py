from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO

app3 = Flask(__name__)


def plot_circle(center, radius, label=None, color='blue'):
    theta = np.linspace(0, 2 * np.pi, 100)
    x = center.real + radius * np.cos(theta)
    y = center.imag + radius * np.sin(theta)
    plt.plot(x, y, label=label, color=color)
    plt.scatter(center.real, center.imag, color=color)  # Mark center with a dot


def plot_line(a, b, label=None):
    z = np.linspace(-10, 10, 100)
    w = a * z + b
    plt.plot(z, w, label=label)


@app3.route('/', methods=['GET', 'POST'])
def index3():
    if request.method == 'POST':
        # Get form inputs
        o = complex(request.form['center'])
        r = float(request.form['radius'])
        a = complex(request.form['a'])
        b = complex(request.form['b'])

        # Plot original circle
        plt.figure(figsize=(10, 5))
        plot_circle(o, r, label='Original Circle', color='blue')
        plt.grid(True, linestyle='--', alpha=0.7, which='both', linewidth=0.5)

        plt.axhline(0, color='black', linewidth=1)
        plt.axvline(0, color='black', linewidth=1)

        # Check if the center is not at (0, 0)
        if o != 0:
            new_radius = r * abs(a)
            new_center_shifted = a * o + b
            plot_circle(new_center_shifted, new_radius, label='Final Circle', color='orange')

            plt.axis('equal')

            # Print the center and radius of the final circle
            final_circle_center = str(new_center_shifted)
            final_circle_radius = str(new_radius)

            # Save the plot to a BytesIO object
            img_data = BytesIO()
            plt.savefig(img_data, format='png')
            img_data.seek(0)
            img_base64 = base64.b64encode(img_data.read()).decode('utf-8')
            plt.close()

            return render_template('index3.html', final_circle_center=final_circle_center, o=o, a=a, b=b, r=r,
                                   final_circle_radius=final_circle_radius, plot=img_base64)

        else:
            new_radius = r * abs(a)
            new_center_shifted = o + b
            plot_circle(new_center_shifted, new_radius, label='Final Circle', color='red')

            # Set equal scaling for a more accurate visualization
            plt.axis('equal')

            # Print the center and radius of the final circle
            final_circle_center = str(new_center_shifted)
            final_circle_radius = str(new_radius)

            # Save the plot to a BytesIO object
            img_data = BytesIO()
            plt.savefig(img_data, format='png')
            img_data.seek(0)
            img_base64 = base64.b64encode(img_data.read()).decode('utf-8')
            plt.close()

            return render_template('index3.html', final_circle_center=final_circle_center,
                                   final_circle_radius=final_circle_radius, plot=img_base64)

    return render_template('index3.html')


if __name__ == '__main__':
    app3.run(debug=True)
