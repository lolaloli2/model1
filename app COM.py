import pickle  # Импорт модуля pickle для работы с сериализацией и десериализацией объектов
import streamlit as st  # Импорт модуля streamlit для создания интерактивных веб-приложений
from imdb import IMDb  # Импорт класса IMDb из модуля imdb для работы с базой данных IMDb

# Функция для получения URL-адреса постера фильма из IMDb
def get_movie_poster_url(movie_title):
    ia = IMDb()  # Создание экземпляра класса IMDb
    movies = ia.search_movie(movie_title)  # Поиск фильмов в базе данных IMDb по названию

    if movies:  # Если найдены фильмы
        movie_id = movies[0].movieID  # Получение идентификатора первого найденного фильма
        movie = ia.get_movie(movie_id)  # Получение информации о фильме по его идентификатору

        if 'cover url' in movie.data:  # Если доступен URL адрес обложки
            return movie.data['cover url']  # Возвращаем URL адрес обложки фильма
        elif 'full-size cover url' in movie.data:  # Если доступен URL адрес полноразмерной обложки
            return movie.data['full-size cover url']  # Возвращаем URL адрес полноразмерной обложки фильма
        else:
            return None  # Возвращаем None, если URL адрес обложки не доступен
    else:
        return None  # Возвращаем None, если фильмы не найдены

# Функция для рекомендации похожих фильмов
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]  # Получение индекса выбранного фильма в базе данных
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])  # Сортировка похожих фильмов по степени сходства
    recommended_movie_names = []  # Список рекомендованных фильмов (названия)
    recommended_movie_posters = []  # Список рекомендованных фильмов (URL адреса постеров)
    for i in distances[1:6]:  # Перебор топ-5 похожих фильмов
        # Получение постера фильма
        movie_id = movies.iloc[i[0]].movie_id  # Получение идентификатора фильма
        movie_name = movies.iloc[i[0]].title  # Получение названия фильма
        recommended_movie_posters.append(get_movie_poster_url(movie_name))  # Добавление URL адреса постера в список
        recommended_movie_names.append(movies.iloc[i[0]].title)  # Добавление названия фильма в список

    return recommended_movie_names, recommended_movie_posters  # Возвращаем списки рекомендованных фильмов

# Загрузка предварительно вычисленных данных
movies = pickle.load(open('movies.pkl', 'rb'))  # Загрузка данных о фильмах
similarity = pickle.load(open('similarity.pkl', 'rb'))  # Загрузка данных о степени сходства фильмов

# Streamlit UI
st.markdown("<h1 style='text-align: center;'>Подбор фильмов</h1>", unsafe_allow_html=True)  # Заголовок
st.markdown("<h3 style='text-align: left;'>Найдите интересное кино на основе ваших любимых фильмов!</h3>", unsafe_allow_html=True)  # Описание

movie_list = movies['title'].values  # Получение списка названий фильмов
selected_movie = st.selectbox(
    "Введите или выберите фильм, который вам нравится:",
    movie_list  # Отображение списка фильмов в виджете выбора
)

if st.button('Показать рекомендацию'):  # Обработка события нажатия кнопки
    st.write("Рекомендуемые фильмы на основе ваших интересов:")  # Вывод заголовка
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)  # Получение рекомендаций

    # Создание горизонтального макета с использованием st.columns
    columns = st.columns(len(recommended_movie_names))  # Создание колонок

    for name, poster_url, col in zip(recommended_movie_names, recommended_movie_posters, columns):  # Перебор рекомендованных фильмов и соответствующих постеров
        col.text(name)  # Отображение названия фильма
        if poster_url is not None:  # Если доступен URL адрес постера
            col.image(poster_url, use_column_width=True)  # Отображение постера
        else:
            col.text("Постер недоступен")  # Вывод сообщения о недоступности постера
