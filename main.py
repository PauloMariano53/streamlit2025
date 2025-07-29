import streamlit as st
import pandas as pd

st.set_page_config(page_title='Finanças',page_icon='💰')

st.text('Olá Mundo!')

st.markdown('''
# BOAS VINDAS!
## NOSSO APP Financeiro!

Expero que curta a experiência
''')


file_upload = st.file_uploader(label='Faça upload dos dados aqui',type='csv')
if file_upload:
    #leitura dos dados
    df = pd.read_csv(file_upload)
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y').dt.date
    
    #exibição dos dados
    exp1 = st.expander('Dados Brutos')
    columns_fmt ={'Valor': st.column_config.NumberColumn('Valor',format="dollar")}
    exp1.dataframe(df,hide_index=True,column_config=columns_fmt)
     
    #Visao isntitiuição
    exp2=st.expander('Intituições')
    df_instituicao = df.pivot_table(index='Data', columns='Instituição', values='Valor')
    
    tab_data,tab_history,tab_share = exp2.tabs(['Dados','Histórico','Distribuição'])

    with tab_data:
        st.dataframe(df_instituicao)

    with tab_history:
        st.line_chart(df_instituicao)
    
    with tab_share:

        date=st.selectbox('Filtro data',options=df_instituicao.index)

        
       # date = st.date_input('Data para distribuição',
       #                     min_value=df_instituicao.index.min(),
       #                     max_value=df_instituicao.index.max())
      
       
        if date not in df_instituicao.index:
            st.warning('Selecione uma data válida')
        #obetm a última data de dados, para o gráfico
        else:
            st.bar_chart(df_instituicao.loc[date])
    