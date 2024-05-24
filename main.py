import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
st.set_option('deprecation.showPyplotGlobalUse', False)
import plotly.graph_objs as go
#
# #uncomment this line if you use mysql
# from query import *

st.set_page_config(page_title="Многомерный анализ KPI",page_icon="📚",layout="wide")
st.title("📊Многомерный анализ KPI для отраслей производства")

# # все графики, которые мы используем, не имеют потоковой подсветки
# theme_plotly = None

# # загружаем стиль css
# with open('style.css')as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#раскомментировать если используем MySQL
#result = view_all_data()
#df=pd.DataFrame(result,columns=["Policy","Expiry","Location","State","Region","Investment","Construction","BusinessType","Earthquake","Flood","Rating","id"])

#грузим excel | в комментарий изменить если подлючаем mysql
# df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# Добавляем лого
st.sidebar.image('logo_1.png', caption='ФКУ НИИ ФСИН РОССИИ©')

# Название сайдабара
st.sidebar.title('Установите срезы данных ниже:')

uploaded_file_xls = st.sidebar.file_uploader("***Добавить файл в формате xlsx,xls***", type=["xlsx", "xls"])
if uploaded_file_xls is not None:
    df = pd.read_excel(uploaded_file_xls)

    region = st.sidebar.multiselect(
        "📌Выберите Федеральный округ",
        options=df["Федеральный_округ"].unique(),
        default=df["Федеральный_округ"].unique(),
    )
    construction = st.sidebar.multiselect(
        "📌Выберите отрасль производства",
        options=df["Отрасль"].unique(),
        default=df["Отрасль"].unique(),
    )
    location = st.sidebar.multiselect(
        "📌Выберите год",
        options=df["Год"].unique(),
        default=df["Год"].unique(),
    )
    Month = st.sidebar.multiselect(
        "📌Выберите месяц",
        options=df["Месяц"].unique(),
        default=df["Месяц"].unique(),
    )
    df_selection = df.query("Федеральный_округ==@region & Год==@location & Месяц==@Month & Отрасль==@construction")

    Year_exp = st.sidebar.multiselect(
        "📌ДОПОЛНИТЕЛЬНО: выберите годовой сравнительный срез:",
        options=df["Год"].unique(),
        default=df["Год"].unique()
    )

    df_selection_exp = df.query("Федеральный_округ==@region & Год==@Year_exp & Месяц==@Month & Отрасль==@construction")

else:
    st.title(body=":red-background[ ❌📚 Пожалуйста, введите данные через кнопку Browse files]")








#переключатель






# вид данных
# st.dataframe(df_selection)



#далее функции выполняют описательный анализ, такой как среднее, режим, сумма
# Разбираемся с объемами производства
def Manufacturing():
    with st.expander("📈Открыть данные"):
        showData=st.multiselect('Filter: ',df_selection.columns,default=["Федеральный_округ", "Отрасль", "Год","Месяц", "Объем_производства", "Оборудование", "Аренда", "Остатки_продукции","Брак", "Чистая_прибыль", "Сумма_контрактов"])
    st.dataframe(df_selection[showData],use_container_width=True)
    #compute top analytics
    sum_manufacturing = float(pd.Series(df_selection['Объем_производства']).sum())
    sum_manufacturing_exp = float(pd.Series(df_selection_exp['Объем_производства']).sum())
    mean_manufacturing = float(pd.Series(df_selection['Объем_производства']).mean())
    mean_manufacturing_exp = float(pd.Series(df_selection_exp['Объем_производства']).mean())
    median_manufacturing = float(pd.Series(df_selection['Объем_производства']).median())
    median_manufacturing_exp = float(pd.Series(df_selection_exp['Объем_производства']).median())
    max_manufacturing = float(pd.Series(df_selection['Объем_производства']).max())
    min_manufacturing = float(pd.Series(df_selection['Объем_производства']).min())
    std_manufacturing = float(pd.Series(df_selection['Объем_производства']).std())
    var_manufacturing = float(pd.Series(df_selection['Объем_производства']).var())
    quantiles_manufacturing = pd.Series(df_selection['Объем_производства']).quantile([0.05, 0.25, 0.5, 0.75, 0.95])
    #добавить минимум и максимум???
    #добавить квантили????
    st.header('1️⃣🛠Статистические метрики для объемов производств:')
    st.write("(Объем производства товаров, выполненных работ и оказанных услуг, связанный с привлечением осужденных к труду, в фактических ценах (включая производство товаров, выполненных работ и оказанных услуг), (тыс.руб). Годовой сравнительный срез - позволяет сравнить выбранные метрики (отраслей производства, месяцев, Федеральных округов) в разные годы ")
    st.write("Годовой сравнительный срез - позволяет сравнить выбранные метрики (отраслей производства, месяцев, Федеральных округов) в разные годы")
    total1,total2,total3,total4,total5,total6=st.columns(6,gap="small")
    with total1:
        if sum_manufacturing>sum_manufacturing_exp:
            sum_exp="inverse"
        else:
            sum_exp="normal"
        if sum_manufacturing==sum_manufacturing_exp:
            sum_exp="off"
        st.metric(label="🟩:green-background[🛠Сумма]" , value=f"{sum_manufacturing:,.0f}", delta=f"Годовой сравнительный срез: {sum_manufacturing_exp:,.0f}", delta_color=sum_exp )
    with total2:
        if mean_manufacturing>mean_manufacturing_exp:
            mean_exp="inverse"
        else:
            mean_exp="normal"
        if mean_manufacturing==mean_manufacturing_exp:
            mean_exp="off"
        st.metric(label="🟩:green-background[🛠Среднее арифметическое]",value=f"{mean_manufacturing:,.0f}", delta=f"Годовой сравнительный срез: {mean_manufacturing_exp:,.0f}", delta_color=mean_exp)
    with total3:
        if median_manufacturing > median_manufacturing_exp:
            median_exp = "inverse"
        else:
            median_exp = "normal"
        if median_manufacturing == median_manufacturing_exp:
            median_exp = "off"
        st.metric(label="🟩:green-background[🛠Медиана]",value=f"{median_manufacturing:,.0f}", delta=f"Годовой сравнительный срез: {median_manufacturing_exp:,.0f}", delta_color=median_exp)
    with total4:
          st.metric(label="🟩:green-background[🛠Максимум]",value=f"{max_manufacturing:,.0f}")
    with total5:
        st.metric(label="🟩:green-background[🛠Минимум]", value=f"{min_manufacturing:,.0f}")
    with total6:
          st.metric(label="🟩:green-background[🛠Стандартное отклонение]",value=f"{ std_manufacturing:,.0f}")

    # total7, total8,total9, total10,total11, total12 = st.columns(6, gap="small")
    # with total7:
    #       st.metric(label="Дисперсия",value=f"{var_manufacturing:,.0f}")
    # with total8:
    #       st.metric(label="5-й процентиль",value=f"{quantiles_manufacturing[0.05]:,.0f}")
    # with total9:
    #       st.metric(label="25-й процентиль",value=f"{quantiles_manufacturing[0.25]:,.0f}")
    # with total10:
    #       st.metric(label="50-й процентиль",value=f"{quantiles_manufacturing[0.5]:,.0f}")
    # with total11:
    #     st.metric(label="75-й процентиль", value=f"{quantiles_manufacturing[0.75]:,.0f}")
    # with total12:
    #       st.metric(label="95-й процентиль",value=f"{quantiles_manufacturing[0.95]:,.0f}")



# style_metric_cards(background_color="#e5efff", border_left_color="#254f77", border_color="#254f77",
#                    box_shadow="#254f77")

def graphs():
    investment_mean_by_district = df_selection.groupby("Федеральный_округ")["Объем_производства"].sum().reset_index()


    fig_1 = px.bar(
        investment_mean_by_district,
        x="Объем_производства",
        y="Федеральный_округ",
        orientation="h",
        title="<b>Средний объем производства по федеральным округам</b>",
        color_discrete_sequence=["#0083B8"] * len(investment_mean_by_district),
        template="plotly_white"
    )

    fig_1.update_layout(
        font=dict(
            size=18,  # Увеличиваем размер шрифта
            color='black'  # Устанавливаем цвет шрифта черным
        ),
        title_font=dict(
            size=24,  # Увеличиваем размер шрифта заголовка
            color='black'  # Устанавливаем цвет шрифта заголовка черным
        ),
        xaxis=dict(
            title_font=dict(
                size=20,  # Увеличиваем размер шрифта подписи оси X
                color='black'  # Устанавливаем цвет шрифта подписи оси X черным
            ),
            tickfont=dict(
                size=18,  # Увеличиваем размер шрифта меток оси X
                color='black'  # Устанавливаем цвет шрифта меток оси X черным
            )
        ),
        yaxis=dict(
            title_font=dict(
                size=20,  # Увеличиваем размер шрифта подписи оси Y
                color='black'  # Устанавливаем цвет шрифта подписи оси Y черным
            ),
            tickfont=dict(
                size=18,  # Увеличиваем размер шрифта меток оси Y
                color='black'  # Устанавливаем цвет шрифта меток оси Y черным
            )
        )
    )

    fig_2 = px.pie(df_selection, values='Объем_производства', names='Отрасль', title='Отрасли по объемам производства')
    fig_2.update_layout(legend_title="Regions", legend_y=0.9)
    fig_2.update_traces(textinfo='percent+label', textposition='inside')

    fig_2.update_layout(
        legend_title="Regions",
        legend_y=0.9,
        font=dict(
            size=20,  # Увеличиваем размер шрифта
            color='black'  # Устанавливаем цвет шрифта черным
        ),
        title_font=dict(
            size=24,  # Увеличиваем размер шрифта заголовка
            color='black'  # Устанавливаем цвет шрифта заголовка черным
        ),
        legend=dict(
            font=dict(
                size=20,  # Увеличиваем размер шрифта легенды
                color='black'  # Устанавливаем цвет шрифта легенды черным
            )
        )
    )

    fig_2.update_traces(
        textinfo='percent+label',
        textposition='inside',
        textfont=dict(
            size=20,  # Увеличиваем размер шрифта текста внутри секций
            color='black'  # Устанавливаем цвет текста внутри секций черным
        )
    )

    col1, col2 = st.columns([1, 1], gap='small')

    # Отображение графиков в колонках
    with col1:
        st.plotly_chart(fig_1)

    with col2:
        st.plotly_chart(fig_2)



        # fig.update_layout(
        #     font=dict(
        #         size=25,
        #         color='black'  # устанавливаем размер шрифта
        #     ),
        #     margin=dict(l=150, r=150, t=50, b=50)
        # )







def Costs_and_cash():
    sum_cash = float(pd.Series(df_selection['Чистая_прибыль']).sum())
    sum_cash_exp = float(pd.Series(df_selection_exp['Чистая_прибыль']).sum())
    mean_cash = float(pd.Series(df_selection['Чистая_прибыль']).mean())
    mean_cash_exp = float(pd.Series(df_selection_exp['Чистая_прибыль']).mean())
    median_cash = float(pd.Series(df_selection['Чистая_прибыль']).median())
    median_cash_exp = float(pd.Series(df_selection_exp['Чистая_прибыль']).median())
    max_manufacturing = float(pd.Series(df_selection['Чистая_прибыль']).max())
    min_manufacturing = float(pd.Series(df_selection['Чистая_прибыль']).min())
    std_manufacturing = float(pd.Series(df_selection['Чистая_прибыль']).std())
    # var_manufacturing = float(pd.Series(df_selection['Чистая_прибыль']).var())
    # quantiles_manufacturing = pd.Series(df_selection['Чистая_прибыль']).quantile([0.05, 0.25, 0.5, 0.75, 0.95])

    #добавить минимум и максимум
    #добавить квантили

    st.header('2️⃣💰Статистический анализ чистой прибыли:')
    st.write("(Превышение доходов над расходами (прибыль) от деятельности, связанной с привлечением осужденных к труду, (тыс. руб))")
    total1,total2,total3,total4,total5,total6=st.columns(6,gap="small")
    with total1:
        if sum_cash > sum_cash_exp:
            sum_cash_exp_dc = "inverse"
        else:
            sum_cash_exp_dc = "normal"
        if sum_cash == sum_cash_exp:
            sum_cash_exp_dc = "off"
        st.metric(label="🟦 :blue-background[💰Сумма]", value=f"{sum_cash:,.0f}", delta=f"Годовой сравнительный срез:{sum_cash_exp:,.0f}", delta_color=sum_cash_exp_dc)
    with total2:
        if mean_cash > mean_cash_exp:
            mean_cash_exp_dc = "inverse"
        else:
            mean_cash_exp_dc = "normal"
        if mean_cash == mean_cash_exp:
            mean_cash_exp_dc = "off"
        st.metric(label="🟦 :blue-background[💰Среднее арифметическое]",value=f"{mean_cash:,.0f}", delta=f"Годовой сравнительный срез:{mean_cash_exp:,.0f}", delta_color=mean_cash_exp_dc)
    with total3:
        if median_cash > median_cash_exp:
            median_cash_exp_dc = "inverse"
        else:
            median_cash_exp_dc = "normal"
        if median_cash == median_cash_exp:
            median_cash_exp_dc = "off"
        st.metric(label="🟦 :blue-background[💰Медиана]",value=f"{median_cash:,.0f}", delta=f"Годовой сравнительный срез:{median_cash_exp:,.0f}", delta_color=median_cash_exp_dc)
    with total4:
          st.metric(label="🟦 :blue-background[💰Максимум]",value=f"{max_manufacturing:,.0f}")
    with total5:
        st.metric(label="🟦 :blue-background[💰Минимум]", value=f"{min_manufacturing:,.0f}")
    with total6:
          st.metric(label="🟦 :blue-background[💰Стандартное отклонение]",value=f"{ std_manufacturing:,.0f}")

    # total7, total8,total9, total10,total11, total12 = st.columns(6, gap="small")
    # with total7:
    #       st.metric(label="Дисперсия",value=f"{var_manufacturing:,.0f}")
    # with total8:
    #       st.metric(label="5-й процентиль",value=f"{quantiles_manufacturing[0.05]:,.0f}")
    # with total9:
    #       st.metric(label="25-й процентиль",value=f"{quantiles_manufacturing[0.25]:,.0f}")
    # with total10:
    #       st.metric(label="50-й процентиль",value=f"{quantiles_manufacturing[0.5]:,.0f}")
    # with total11:
    #     st.metric(label="75-й процентиль", value=f"{quantiles_manufacturing[0.75]:,.0f}")
    # with total12:
    #       st.metric(label="95-й процентиль",value=f"{quantiles_manufacturing[0.95]:,.0f}")

def graphs_cash():
    investment_mean_by_district = df_selection.groupby("Федеральный_округ")["Чистая_прибыль"].sum().reset_index()

    fig_investment_mean = px.bar(
        investment_mean_by_district,
        x="Чистая_прибыль",
        y="Федеральный_округ",
        orientation="h",
        title="<b>Чистая прибыль в разрезе федеральных округов</b>",
        color_discrete_sequence=["#0083B8"] * len(investment_mean_by_district),
        template="plotly_white",
    )

    fig_investment_mean.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
    )

    right, center, left = st.columns(3)
    right.plotly_chart(fig_investment_mean, use_container_width=True)

    with center:
        fig_2 = px.parallel_categories(df_selection, dimensions=["Отрасль", "Федеральный_округ"], title="Федеральные округа, которые содержат определенные отрасли", color_continuous_scale=px.colors.sequential.Inferno)
        st.plotly_chart(fig_2, use_container_width=True)

    with left:
        # круговая диаграмма
        fig = px.pie(df_selection, values='Чистая_прибыль', names='Отрасль', title='Чистая прибыль в разрезе отраслей')
        fig.update_layout(legend_title="Regions", legend_y=0.9)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True)



#Проводим аналогичные манипуляции для параметра общей суммы контрактов
def Contract():
    st.header('3️⃣ 📃 Анализ заключенных контрактов для производств:')
    st.write("(Объем заказов (контрактов) на поставку продукции, выполнение работ и оказание услуг в последующем периоде в ЦТАО, УПМ, ЛПМ, участках, текущего года тыс. руб.)")
    sum_contract = float(pd.Series(df_selection['Сумма_контрактов']).sum())
    sum_contract_exp = float(pd.Series(df_selection_exp['Сумма_контрактов']).sum())
    mean_contract = float(pd.Series(df_selection['Сумма_контрактов']).mean())
    mean_contract_exp = float(pd.Series(df_selection_exp['Сумма_контрактов']).mean())
    median_contract = float(pd.Series(df_selection['Сумма_контрактов']).median())
    median_contract_exp = float(pd.Series(df_selection_exp['Сумма_контрактов']).median())
    max_contract = float(pd.Series(df_selection['Сумма_контрактов']).max())
    min_contract = float(pd.Series(df_selection['Сумма_контрактов']).min())
    std_contract = float(pd.Series(df_selection['Сумма_контрактов']).std())
    # var_manufacturing = float(pd.Series(df_selection['Сумма_контрактов']).var())
    # quantiles_manufacturing = pd.Series(df_selection['Сумма_контрактов']).quantile([0.05, 0.25, 0.5, 0.75, 0.95])

    total1,total2,total3,total4,total5,total6=st.columns(6,gap="small")
    with total1:
        if sum_contract>sum_contract_exp:
            sum_c_exp="inverse"
        else:
            sum_c_exp="normal"
        if sum_contract==sum_contract_exp:
            sum_c_exp="off"
        st.metric(label="🟧:orange-background[📃Сумма]", value=f"{sum_contract:,.0f}", delta=f"Годовой сравнительный срез:{sum_contract_exp:,.0f}", delta_color=sum_c_exp)
    with total2:
        if mean_contract>mean_contract_exp:
            mean_c_exp="inverse"
        else:
            mean_c_exp="normal"
        if mean_contract==mean_contract_exp:
            mean_c_exp="off"
        st.metric(label="🟧:orange-background[📃Среднее арифметическое]",value=f"{mean_contract:,.0f}", delta=f"Годовой сравнительный срез:{mean_contract_exp:,.0f}", delta_color=mean_c_exp)
    with total3:
        if median_contract > median_contract_exp:
            median_c_exp = "inverse"
        else:
            median_c_exp = "normal"
        if sum_contract == sum_contract_exp:
            median_c_exp = "off"
        st.metric(label="🟧:orange-background[📃Медиана]",value=f"{median_contract:,.0f}", delta=f"Годовой сравнительный срез:{median_contract_exp:,.0f}", delta_color=median_c_exp)
    with total4:
          st.metric(label="🟧:orange-background[📃Максимум]",value=f"{max_contract:,.0f}")
    with total5:
        st.metric(label="🟧:orange-background[📃Минимум]", value=f"{min_contract:,.0f}")
    with total6:
          st.metric(label="🟧:orange-background[📃Стандартное отклонение]",value=f"{ std_contract:,.0f}")

def graphs_contrakt():
    investment_mean_by_district = df_selection.groupby("Федеральный_округ")["Сумма_контрактов"].sum().reset_index()

    fig_investment_mean = px.bar(
        investment_mean_by_district,
        x="Сумма_контрактов",
        y="Федеральный_округ",
        orientation="h",
        title="<b>Объем контрактов в разрезе федеральных округов</b>",
        color_discrete_sequence=["#0083B8"] * len(investment_mean_by_district),
        template="plotly_white",
    )

    fig_investment_mean.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
    )

    right, center, left = st.columns(3)
    right.plotly_chart(fig_investment_mean, use_container_width=True)

    with center:
        fig_2 = px.parallel_categories(df_selection, dimensions=["Отрасль", "Федеральный_округ"], title="Федеральные округа, которые содержат определенные отрасли", color_continuous_scale=px.colors.sequential.Inferno)
        st.plotly_chart(fig_2, use_container_width=True)

    with left:
        # круговая диаграмма
        fig = px.pie(df_selection, values='Сумма_контрактов', names='Отрасль', title='Объем контрактов в разрезе отраслей')
        fig.update_layout(legend_title="Regions", legend_y=0.9)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True)

def remains():
    st.header('4️⃣ 📦 Остатки готовой продукции производства:')
    st.write("(Остатки готовой продуции собственного производства в ЦТАО, УПМ, ЛПМ, участках на конец отчетного периода, тыс. руб.)")

def arenda():
    st.header('5️⃣🏢 Месячная сумма аренды площадей:')
    # st.write("(Остатки готовой продуции собственного производства в ЦТАО, УПМ, ЛПМ, участках на конец отчетного периода, тыс. руб.)")

def arenda_tools():
    st.header('6️⃣🚜 Количество арендованного оборудования, ед_:')
    # st.write("(Остатки готовой продуции собственного производства в ЦТАО, УПМ, ЛПМ, участках на конец отчетного периода, тыс. руб.)")

def brak():
    st.header('7️⃣❎ Объем бракованной продукции:')
    # st.write("(Остатки готовой продуции собственного производства в ЦТАО, УПМ, ЛПМ, участках на конец отчетного периода, тыс. руб.)")

def human():
    st.header('8️⃣👤️️Среднесписочная численность осужденных, привлеченных к труду:')
    # st.write("(Остатки готовой продуции собственного производства в ЦТАО, УПМ, ЛПМ, участках на конец отчетного периода, тыс. руб.)")

def human_hour():
    st.header('9️⃣🕓 Количество отработанных человеко-часов:')

# #
# st.subheader('▶  Анализ распределений ')
# graphs

#
# #функция для отображения текущей прибыли относительно ожидаемой цели
# # закомментировал так как считаю это тут лишнее
# # def Progressbar():
# #     st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
# #     target=3000000000
# #     current=df_selection["Investment"].sum()
# #     percent=round((current/target*100))
# #     mybar=st.progress(0)
# #
# #     if percent>100:
# #         st.subheader("Target done !")
# #     else:
# #      st.write("you have ",percent, "% " ,"of ", (format(target, 'd')), "TZS")
# #      for percent_complete in range(percent):
# #         time.sleep(0.1)
# #         mybar.progress(percent_complete+1,text=" Target Percentage")
# #
# # #menu bar
# # def sideBar():
# #  with st.sidebar:
# #     selected=option_menu(
# #         menu_title="Main Menu",
# #         options=["Home","Progress"],
# #         icons=["house","eye"],
# #         menu_icon="cast",
# #         default_index=0
# #     )
# #  if selected=="Home":
# #     #st.subheader(f"Page: {selected}")
# #     Home()
# #     graphs()
# #  if selected=="Progress":
# #     #st.subheader(f"Page: {selected}")
# #     Progressbar()
# #     graphs()
#
# # sideBar()

# ДИАГРАММА СВЯЗЕЙ
def porcoords():
    st.header('▶ 📈📉Диаграмма связей (KPI+Федеральные округа+Отрасли)')

    fig_5 = go.Figure(data=go.Parcoords(
        line_color='red',
        dimensions=[
        dict(range=[df_selection['Объем_производства'].min(), df_selection['Объем_производства'].max()],
             label='Объем_производства', values=df_selection['Объем_производства']),
        dict(range=[df_selection['Чистая_прибыль'].min(), df_selection['Чистая_прибыль'].max()],
             label='Чистая_прибыль', values=df_selection['Чистая_прибыль']),

        dict(range=[1, len(df_selection['Отрасль'].unique())],  # задаем диапазон значений для оси Округ
             tickvals=list(range(1, len(df_selection['Отрасль'].unique()) + 1)),  # устанавливаем значения меток
             ticktext=df_selection['Отрасль'].unique(),  # устанавливаем текст меток
             label='Отрасль', values=df_selection['Отрасль'].apply(lambda x: df_selection['Отрасль'].unique().tolist().index(x) + 1)),

        dict(range=[1, len(df_selection['Федеральный_округ'].unique())],  # задаем диапазон значений для оси Округ
             tickvals=list(range(1, len(df_selection['Федеральный_округ'].unique()) + 1)),  # устанавливаем значения меток
             ticktext=df_selection['Федеральный_округ'].unique(),  # устанавливаем текст меток
             label='Федеральный_округ', values=df_selection['Федеральный_округ'].apply(
                lambda x: df_selection['Федеральный_округ'].unique().tolist().index(x) + 1)),
        dict(range=[df_selection['Сумма_контрактов'].min(), df_selection['Сумма_контрактов'].max()],
             label='Сумма_контрактов', values=df_selection['Сумма_контрактов'])
        ]
    ))

    fig_5.update_layout(
        font=dict(
            size=25,
            color='black'  # устанавливаем размер шрифта
        ),
        margin=dict(l=150, r=150, t=50, b=50)
    )


    fig_6 = go.Figure(data=go.Parcoords(
        line_color='blue',
        dimensions=[
        dict(range=[df_selection_exp['Объем_производства'].min(), df_selection_exp['Объем_производства'].max()],
             label='Объем_производства', values=df_selection_exp['Объем_производства']),
        dict(range=[df_selection_exp['Чистая_прибыль'].min(), df_selection_exp['Чистая_прибыль'].max()],
             label='Чистая_прибыль', values=df_selection_exp['Чистая_прибыль']),

        dict(range=[1, len(df_selection_exp['Отрасль'].unique())],  # задаем диапазон значений для оси Округ
             tickvals=list(range(1, len(df_selection_exp['Отрасль'].unique()) + 1)),  # устанавливаем значения меток
             ticktext=df_selection_exp['Отрасль'].unique(),  # устанавливаем текст меток
             label='Отрасль', values=df_selection_exp['Отрасль'].apply(lambda x: df_selection_exp['Отрасль'].unique().tolist().index(x) + 1)),

        dict(range=[1, len(df_selection_exp['Федеральный_округ'].unique())],  # задаем диапазон значений для оси Округ
             tickvals=list(range(1, len(df_selection_exp['Федеральный_округ'].unique()) + 1)),  # устанавливаем значения меток
             ticktext=df_selection_exp['Федеральный_округ'].unique(),  # устанавливаем текст меток
             label='Федеральный_округ', values=df_selection_exp['Федеральный_округ'].apply(
                lambda x: df_selection_exp['Федеральный_округ'].unique().tolist().index(x) + 1)),
        dict(range=[df_selection_exp['Сумма_контрактов'].min(), df_selection_exp['Сумма_контрактов'].max()],
             label='Сумма_контрактов', values=df_selection_exp['Сумма_контрактов'])
        ]
    ))

    fig_6.update_layout(
        font=dict(
            size=25,
            color='black'  # устанавливаем размер шрифта
        ),
        margin=dict(l=150, r=150, t=50, b=50)
    )

    unique_years = ", ".join(map(str, df_selection['Год'].unique()))
    st.subheader(f"Выбран годовой период: {unique_years}")

    st.plotly_chart(fig_5, use_container_width=True)

    if not df_selection_exp['Год'].empty:
        unique_years_exp = ", ".join(map(str, df_selection_exp['Год'].unique()))
        st.subheader(f"Выбран годовой период для сравнения: {unique_years_exp}")
        st.plotly_chart(fig_6, use_container_width=True)
    else:
        st.subheader("❌Выберите годовой период для сравнения❌")

def fig11():
    # matrix1,matrix2=st.columns(2,gap="small")
    st.header('▶ 📈📉Матрицы взаимных распределений')

    fig3 = px.scatter_matrix(df_selection, dimensions=["Объем_производства", "Чистая_прибыль", "Сумма_контрактов"], color="Федеральный_округ",  symbol='Отрасль', title='Матрица взаимных распределений для Федеральных округов', width=2000, height=1500)



    # делаем крупнее точки
    for trace in fig3.data:
        trace.update(marker=dict(size=10))

    # Настройка подписей
    fig3.update_layout(
        title=dict(
            font=dict(
                size=20  # Размер заголовка
            )
        ),
        legend=dict(
            font=dict(
                size=20  # Размер текста легенды
            )
        )
    )

    fig3.update_traces(marker={"size": 20, "opacity": 0.7})
    fig3.for_each_xaxis(lambda axis: axis.update(title={
        "font": {"size": 20}}))

    # # Настройка подписей осей (черный цвет и размер 14)
    # for dim in fig3.data:
    #     dim.update(
    #         marker=dict(size=30),  # Размер точек
    #         selector=dict(type='scatter')
    #     )



    # Отображение графика
    st.plotly_chart(fig3)


    # fig4 = px.scatter_matrix(df_selection, dimensions=["Объем_производства", "Чистая_прибыль", "Сумма_контрактов"], color="Отрасль")
    #
    # col1,col2 = st.columns(2,gap='small')
    #
    # with col1:
    # st.plotly_chart(fig3)

    # with col2:
    #     st.plotly_chart(fig4)

#
def Fig12():
    st.header('▶ 📈📉Коробчатые диаграммы (отрасли производства)')
    # feature_x = st.selectbox('Select feature for x Qualitative data', df_selection.select_dtypes("object").columns)
    feature_y = st.selectbox('Выберите функцию для количественных данных', df_selection.select_dtypes("number").columns,key="feature_y")
    fig2 = go.Figure(
        data=[go.Box(x=df_selection['Отрасль'], y=df[feature_y])],
        layout=go.Layout(
            title=go.layout.Title(text="ВИДЫ ОТРАСЛЕЙ ПРОИЗВОДСТВА"),
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
            xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
            yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
            font=dict(color='#cecdcd'),  # Set text color to black
        )
    )
    # Display the Plotly figure using Streamlit
    st.plotly_chart(fig2,use_container_width=True)



def Fig13():
    st.header('▶ 📈📉Коробчатые диаграммы (Федеральные округа)')
    # feature_x = st.selectbox('Select feature for x Qualitative data', df_selection.select_dtypes("object").columns)
    feature_y3 = st.selectbox('Выберите функцию для количественных данных', df_selection.select_dtypes("number").columns,key="feature_y3")
    fig3 = go.Figure(
        data=[go.Box(x=df_selection['Федеральный_округ'], y=df[feature_y3])],
        layout=go.Layout(
            title=go.layout.Title(text="ФЕДЕРАЛЬНЫЕ ОКРУГА"),
            plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
            paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
            xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
            yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
            font=dict(color='#cecdcd'),  # Set text color to black
        )
    )
    # Display the Plotly figure using Streamlit
    st.plotly_chart(fig3,use_container_width=True)

# ОБРАБОТКА ОШИБОК КОГДА ЧАСТЬ СРЕЗОВ НЕ ЗАПОЛНЕНЫ!

# if df_selection.empty:
#     st.title(body=":red-background[❌Ошибка!❌ Пожалуйста, заполните срезы данных!📚]")
# else:
#     Manufacturing()
#     graphs()
#     Costs_and_cash()
#     Contract()
#     Fig12()
#     Fig13()


if uploaded_file_xls is not None:
    if df_selection.empty:
        st.title(body=":red-background[❌Ошибка!❌ Пожалуйста, заполните срезы данных!📚]")
    else:

        Manufacturing()
        graphs()
        Costs_and_cash()
        graphs_cash()
        Contract()
        graphs_contrakt()
        remains()
        arenda()
        arenda_tools()
        human()
        human_hour()
        brak()
        porcoords()
        fig11()
        Fig12()
        Fig13()


# 👤
#theme
hide_st_style="""

<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
</style>
"""

# streamlit run "C:\Python - Streamlit Project\main.py"
