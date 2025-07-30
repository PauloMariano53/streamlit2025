import streamlit as st
import pandas as pd



def calc_general_stats(df):
    df_data = df.groupby(by='Data')[['Valor']].sum()
    df_data['lag_1'] = df_data['Valor'].shift(1)
    df_data['diferença Mensal'] = df_data['Valor'] -df_data ['lag_1']
    df_data['Média 6 M diferença Mensal'] = df_data['diferença Mensal'].rolling(6).mean()
    df_data['Média 12 M diferença Mensal'] = df_data['diferença Mensal'].rolling(12).mean()
    df_data['Média 24 M diferença Mensal'] = df_data['diferença Mensal'].rolling(24).mean()
    df_data['Média 6 M TOTAL'] = df_data['Valor'].rolling(6).apply(lambda x: x[-1] - x[0])
    df_data['Média 12 M TOTAL'] = df_data['Valor'].rolling(12).apply(lambda x: x[-1] - x[0])
    df_data['Média 24 M TOTAL'] = df_data['Valor'].rolling(24).apply(lambda x: x[-1] - x[0])
    return df_data




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


    # Abas para distribuição dos dados
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
    

    
    df_stats = calc_general_stats(df)
    st.dataframe(df_stats)


