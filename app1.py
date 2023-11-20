from flask import Flask, render_template, request
import math
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app1 = Flask(__name__)


@app1.route('/', methods=['GET', 'POST'])
def index1():
    if request.method == 'POST':
        a = complex(request.form['a'])
        b = complex(request.form['b'])
        z = complex(request.form['z'])
        w = reflection_function(a, b, z)
        n = calculate_result(z, w)

        # Grafik
        z_real, z_imag = np.real(z), np.imag(z)
        w_real, w_imag = np.real(w), np.imag(w)

        # chizma yaratish
        plt.figure(figsize=(10, 5))
        plt.grid(True, linestyle='--', alpha=0.5, which='both', linewidth=0.5)

        # koordinata o'lchami
        real_min = min(z_real, w_real, 0) - 1
        real_max = max(z_real, w_real, 0) + 1
        imag_min = min(z_imag, w_imag, 0) - 1
        imag_max = max(z_imag, w_imag, 0) + 1

        # haqiqiy va mavhum o'qlar
        plt.plot([real_min, real_max], [0, 0], 'k')
        plt.plot([0, 0], [imag_min, imag_max], 'k')

        # Grafik o'lchamini avtomatik qilish
        plt.xlim([real_min, real_max])
        plt.ylim([imag_min, imag_max])

        plt.quiver(0, 0, z_real, z_imag, angles='xy', scale_units='xy', scale=1, color='blue', label='z')
        plt.quiver(0, 0, w_real, w_imag, angles='xy', scale_units='xy', scale=1, color='red', label='w=a•z+b')

        # Add labels and legend
        plt.xlabel('Im(z)')
        plt.ylabel('Re(z)')
        plt.legend()
        # Save the plot to a BytesIO object
        img_data = BytesIO()
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        img_base64 = base64.b64encode(img_data.read()).decode('utf-8')
        plt.close()

        # Display result and plot in the template
        return render_template('index1.html', a=a, b=b, z=z, w=w, n=n, plot=img_base64)

    # Display the form if it's a GET request
    return render_template('index1.html')


def reflection_function(a, b, z):
    return a * z + b


def calculate_result(z, w):
    z_abs = abs(z)
    w_abs = abs(w)

    if w_abs > z_abs:
        return f"The z vector has increased by  {w_abs / z_abs:.3f} times"
    elif w_abs < z_abs:
        return f"The z vector ha decreased by  {z_abs / w_abs:.3f} times"
    else:
        return "Did not change."


if __name__ == '__main__':
    app1.run(debug=True)
