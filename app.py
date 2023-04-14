from flask import Flask, request, render_template
import flask
import pickle
import tensorflow as tf, keras
import pandas as pd

app = Flask(__name__)


@app.route('/')
def choose_prediction_method():
    return render_template('main.html')


def matrix_filler(params):
    params = pd.DataFrame(params).T
    minmax_load = pickle.load(open('./models/minmax_matrix_filler.pkl', 'rb'))
    minmax_scal = minmax_load.transform(params)
    model = tf.keras.models.load_model('./models/matrix_filler')
    minmax_scal = minmax_scal
    pred = model.predict([minmax_scal])
    return pred
    
def tensile_strength(params):
    params = pd.DataFrame(params).T
    minmax_load = pickle.load(open('./models/stand_scal.pkl', 'rb'))
    minmax_scal = minmax_load.transform(params)
    model = tf.keras.models.load_model('./models/tensile_strength')
    minmax_scal = minmax_scal
    pred = model.predict([minmax_scal])
    return pred

def modul_elastic(params):
    params = pd.DataFrame(params).T
    minmax_load = pickle.load(open('./models/minmax.pkl', 'rb'))
    minmax_scal = minmax_load.transform(params)
    model = tf.keras.models.load_model('./models/modul_elastic')
    minmax_scal = minmax_scal
    pred = model.predict([minmax_scal])
    return pred

@app.route('/matrix_filler/', methods=['POST', 'GET'])
def matrix_filler_predict():
    message = ''
    if request.method == 'POST':
        param_list = ('Плотность, кг/м3', 'модуль упругости, ГПа', 'Количество отвердителя, м.%', 
                      'Содержание эпоксидных групп,%_2', 'Температура вспышки, С_2', 'Поверхностная плотность, г/м2', 
                      'Модуль упругости при растяжении, ГПа', 'Прочность при растяжении, МПа', 'Потребление смолы, г/м2',
                      'Угол нашивки, град', 'Шаг нашивки', 'Плотность нашивки')
        params = []
        for i in param_list:
            param = request.form.get(i)
            params.append(param)
        params = [float(i.replace(',', '.')) for i in params]

        message = f'Соотношение матрица-наполнитель для введенных параметров: {matrix_filler(params)}'
    return render_template('matrix_filler.html', message=message)


@app.route('/modul_elastic/', methods=['POST', 'GET'])
def modul_elastic_predict():
    message = ''
    if request.method == 'POST':
        param_list = ('Соотношение матрица-наполнитель', 'Плотность, кг/м3',
                        'модуль упругости, ГПа', 'Количество отвердителя, м.%',
                        'Содержание эпоксидных групп,%_2', 'Температура вспышки, С_2',
                        'Поверхностная плотность, г/м2',
                        'Потребление смолы, г/м2', 'Угол нашивки, град',
                        'Шаг нашивки', 'Плотность нашивки')
        params = []
        for i in param_list:
            param = request.form.get(i)
            params.append(param)
        params = [float(i.replace(',', '.')) for i in params]
        message = f'Модуль упругости при растяжении для введенных параметров: {modul_elastic(params)} ГПа'
    return render_template('modul_elastic.html', message=message)

@app.route('/tensile_strength/', methods=['POST', 'GET'])
def tensile_strength_predict():
    message = ''
    if request.method == 'POST':
        param_list = ('Соотношение матрица-наполнитель', 'Плотность, кг/м3',
                        'модуль упругости, ГПа', 'Количество отвердителя, м.%',
                        'Содержание эпоксидных групп,%_2', 'Температура вспышки, С_2',
                        'Поверхностная плотность, г/м2',
                        'Потребление смолы, г/м2', 'Угол нашивки, град',
                        'Шаг нашивки', 'Плотность нашивки')
        params = []
        for i in param_list:
            param = request.form.get(i)
            params.append(param)
        params = [float(i.replace(',', '.')) for i in params]

        message = f'Прочность при растяжении для введенных параметров: {tensile_strength(params)} МПа'
    return render_template('tensile_strength.html', message=message)


if __name__ == '__main__':
    app.run()
