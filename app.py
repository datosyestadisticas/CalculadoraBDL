import streamlit as st
import pandas as pd
import numpy as np

# Leer archivos CSV
df_2020 = pd.read_csv("BDL2020V2.csv", delimiter=",")
df_2021 = pd.read_csv("BDL2021V2.csv", delimiter=",")

# Configuracion de pagina
st.set_page_config(layout="centered", page_icon="🪪", page_title="Calculadora BDL")

# Seleccion de dataframe segun año
with st.sidebar:
    anio = st.selectbox("Año de consulta",[2020, 2021],index=1)

if anio == 2021:
    consulta = df_2021
else:
    consulta = df_2020

#Titulo de la pagina
st.title("Calculadora Bono Desempeño Laboral AÑO "  + str(anio)  )

# Barra lateral
with st.sidebar:
    regiones = consulta['NOMBRE_REGION'].unique()
    region_choice = st.selectbox("Región del establecimiento", regiones, index=0)
    comunas = consulta['COMUNA'].loc[consulta["NOMBRE_REGION"] == region_choice].unique()
    comuna_choice = st.selectbox("Comuna del establecimiento",comunas,index=0)
    establecimientos = consulta["CODIGO_ESTABLECIMIENTO"].loc[consulta["COMUNA"] == comuna_choice].unique()
    establecimiento_choice = st.selectbox("Establecimiento", establecimientos,index=0) 
    no_anios_servicio = st.selectbox("Años de servicio", ["Mayor a diez años", "Menor o igual a diez años"], index=0)   
    horas_contrato = st.number_input("Ingrese horas de contrato", min_value=0.0, max_value=45.0, value=44.0,step=0.5, format="%.1f")
    escolaridad = st.selectbox("Enseñanza media completa", ["Completa", "Incompleta"], index=0)
    nombre_establecimiento = consulta['NOMBRE_ESTABLECIMIENTO'].loc[consulta["CODIGO_ESTABLECIMIENTO"] == establecimiento_choice].unique()
    asistencia_promedio_anual_establ = 0
    submitted = st.button("Consultar")

st.write(f""" ### Tu selección es la siguiente:

        ESTABLECIMIENTO {establecimiento_choice} - {nombre_establecimiento[0]}

        Año de cálculo: {anio}
        Región del establecimiento: {region_choice}
        Comuna del establecimiento: {comuna_choice}
        Años de servicio de consultante: {no_anios_servicio}
        Horas de contrato del consultante: {horas_contrato}
        Escolaridad consultante: {escolaridad}
""")


if submitted:

    st.success("🎉 Su consulta ha sido generada!")
    get_asistencia_promedio_anual = consulta["ASISTENCIA_PROMEDIO_ANUAL_DEL_ESTABLECIMIENTO"].loc[(consulta["COMUNA"] == comuna_choice) & (consulta["CODIGO_ESTABLECIMIENTO"] == establecimiento_choice)].unique()
    asistencia_promedio_anual_establ = get_asistencia_promedio_anual[0]
    
    
    calculo_anios_servicio = 30 if no_anios_servicio == "Mayor a diez años" else 15
     # Calculo Escolaridad no es una formula es un input
    
    calculo_escolaridad = 20 if escolaridad == "Completa" else 10
    calculo_asistencia = 30 if asistencia_promedio_anual_establ >= 90 else 15
    # Siempre es 0 ?
    calculo_simce = 0
    # Existen rut con ;? o bien se suma solamente
    calculo_ige = calculo_anios_servicio + calculo_escolaridad + calculo_asistencia + calculo_simce

    # st.write(f"""  

    #     Años de servicio: {calculo_anios_servicio}
    #     Calculo escolaridad: {calculo_escolaridad}
    #     Calculo asistencia: {calculo_asistencia}
    #     Calculo IGE: {calculo_ige}
    
    #  """)
    
    if(anio == 2021):
        ochenta_o_mas = 307761
        setentayuno_a_setentaynueve = 270829
        setenta_a_cincuentayuno = 227743
        menor_igual_50 = 184656
    
        if  calculo_ige >= 80:
            valor_segun_tramo_ige = ochenta_o_mas
        elif calculo_ige >= 71:
            valor_segun_tramo_ige = setentayuno_a_setentaynueve
        elif calculo_ige >= 51:
            valor_segun_tramo_ige = setenta_a_cincuentayuno
        else:
            valor_segun_tramo_ige = menor_igual_50
        
        monto_a_pago_segun_horas_contrato = int((valor_segun_tramo_ige / 44) * horas_contrato if horas_contrato < 44 else valor_segun_tramo_ige)


        pago_cuota_1 = int(np.ceil(monto_a_pago_segun_horas_contrato / 2))
        pago_cuota_2 = int(np.floor(monto_a_pago_segun_horas_contrato / 2))

        # st.write("Valores redondedos" + str(np.ceil(monto_a_pago_segun_horas_contrato / 2)) )
        # st.write("Valores redondedos" + str(np.floor(monto_a_pago_segun_horas_contrato / 2)) )
        # st.write("Valores sin redondedos" + str(monto_a_pago_segun_horas_contrato / 2) )
        # st.write("Valores sin redondedos" + str(monto_a_pago_segun_horas_contrato / 2) )

    
    if(anio == 2020):
        ochenta_o_mas = 279806
        cincuentaysesis_a_setentaynueve = 214113
        menor_igual_55 = 164234

        if  calculo_ige >= 80:
            valor_segun_tramo_ige = ochenta_o_mas
        elif calculo_ige >= 56:
            valor_segun_tramo_ige = cincuentaysesis_a_setentaynueve
        elif calculo_ige <= 55:
            valor_segun_tramo_ige = menor_igual_55
        
        monto_a_pago_segun_horas_contrato = int((valor_segun_tramo_ige / 44) * horas_contrato if horas_contrato < 44 else valor_segun_tramo_ige)


        pago_cuota_1 = int(monto_a_pago_segun_horas_contrato / 2)
        pago_cuota_2 = int(monto_a_pago_segun_horas_contrato / 2)

    
    
    st.write(f""" ### La respuesta del sistema es la siguiente: """)

    col1, col2, col3 = st.columns(3)

    col1.metric("Cuota 1","$ {:,d}".format(pago_cuota_1).replace(",",".") )
    col2.metric("Cuota 2","$ {:,d}".format(pago_cuota_2).replace(",",".") )
    col3.metric("Total a pagar","$ {:,d}".format(monto_a_pago_segun_horas_contrato).replace(",",".") )



    st.write(f"""
        * Las cuotas y el valor total a pagar son valores estimados.
        * En caso de presentar dudas comunicarse al correo correo_vtf@junji.cl
     """)

    


        
        




 