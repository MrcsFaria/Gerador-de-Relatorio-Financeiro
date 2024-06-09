import os
import locale
#pip install requests
import requests
#pip install pandas
import pandas as pd
#pip install matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
#pip install reportlab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas

locale.setlocale(locale.LC_TIME,'pt_BR.UTF-8')

dia_atual = datetime.now().strftime("%d-%m-%Y")

diretorio = os.getcwd()

# Função para criar o PDF
def criar_pdf(assunto, usd_atual, eur_atual, btc_atual, usd_var, eur_var, btc_var, usd_alt, eur_alt, btc_alt, usd_baixa, eur_baixa, btc_baixa, caminho_grafico):
    #Criar o PDF
    doc = SimpleDocTemplate(f"Relatório - {dia_atual}.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    #Conteúdo do PDF
    content = []
    content.append(Paragraph('<font size="16"><b>' + assunto + '</b></font><br/><br/>', styles['Heading1']))
    content.append(Paragraph('Prezados,<br/><br/>', styles['Normal']))
    content.append(Paragraph('Segue abaixo o relatório das cotações das moedas Bitcoin (BTC), Dólar Americano (USD) e Euro (EUR) em relação ao Real (BRL) no dia de hoje:<br/><br/>', styles['Normal']))
    
    content.append(Paragraph('<b>Visibilidade das Variações de Hoje:</b><br/>', styles['Normal']))
    content.append(Image(caminho_grafico, width=300, height=250))
    #USD
    content.append(Paragraph('<b>Dólar Americano (USD):</b><br/>', styles['Normal']))
    content.append(Paragraph('- Valor Atual: {}<br/>'.format(usd_atual), styles['Normal']))
    content.append(Paragraph('- Variação: {}%<br/>'.format(usd_var), styles['Normal']))
    content.append(Paragraph('- Alta do Dia: {}<br/>'.format(usd_alt), styles['Normal']))
    content.append(Paragraph('- Baixa do Dia: {}<br/><br/>'.format(usd_baixa), styles['Normal']))

    #Euro
    content.append(Paragraph('<b>Euro (EUR):</b><br/>', styles['Normal']))
    content.append(Paragraph('- Valor Atual: {}<br/>'.format(eur_atual), styles['Normal']))
    content.append(Paragraph('- Variação: {}%<br/>'.format(eur_var), styles['Normal']))
    content.append(Paragraph('- Alta do Dia: {}<br/>'.format(eur_alt), styles['Normal']))
    content.append(Paragraph('- Baixa do Dia: {}<br/><br/>'.format(eur_baixa), styles['Normal']))

    #Bitcoin
    content.append(Paragraph('<b>Bitcoin (BTC):</b><br/>', styles['Normal']))
    content.append(Paragraph('- Valor Atual: {}<br/>'.format(btc_atual), styles['Normal']))
    content.append(Paragraph('- Variação: {}%<br/>'.format(btc_var), styles['Normal']))
    content.append(Paragraph('- Alta do Dia: {}<br/>'.format(btc_alt), styles['Normal']))
    content.append(Paragraph('- Baixa do Dia: {}<br/><br/>'.format(btc_baixa), styles['Normal']))

    content.append(Paragraph('Este relatório é fornecido para fins informativos e não constitui aconselhamento financeiro.<br/>', styles['Normal']))

    doc.build(content)


def principal():
    #Coletando Dados da API
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"

    cotacoes = requests.get(url)
    cotacoes = cotacoes.json()

    dolar = cotacoes['USDBRL']
    euro = cotacoes['EURBRL']
    btc = cotacoes['BTCBRL']

    #Construindo Dataframes
    columns = ['Origem', 'Convertido Para', 'Descrição', 'Alta', 'Baixa', 'Variação', '% Variação', 'Bid', 'Ask', 'timestamp', 'date']

    df_usd = pd.DataFrame([list(dolar.values())], columns=columns)
    df_eur = pd.DataFrame([list(euro.values())], columns=columns)
    df_btc = pd.DataFrame([list(btc.values())], columns=columns)

    df_usd['Alta'] = pd.to_numeric(df_usd['Alta'], errors='coerce')
    df_usd['Baixa'] = pd.to_numeric(df_usd['Baixa'], errors='coerce')
    df_usd['Variação'] = pd.to_numeric(df_usd['Variação'], errors='coerce')
    df_usd['% Variação'] = pd.to_numeric(df_usd['% Variação'], errors='coerce')
    df_usd['Bid'] = pd.to_numeric(df_usd['Bid'], errors='coerce')
    df_usd['Ask'] = pd.to_numeric(df_usd['Ask'], errors='coerce')

    df_eur['Alta'] = pd.to_numeric(df_eur['Alta'], errors='coerce')
    df_eur['Baixa'] = pd.to_numeric(df_eur['Baixa'], errors='coerce')
    df_eur['Variação'] = pd.to_numeric(df_eur['Variação'], errors='coerce')
    df_eur['% Variação'] = pd.to_numeric(df_eur['% Variação'], errors='coerce')
    df_eur['Bid'] = pd.to_numeric(df_eur['Bid'], errors='coerce')
    df_eur['Ask'] = pd.to_numeric(df_eur['Ask'], errors='coerce')

    df_btc['Alta'] = pd.to_numeric(df_btc['Alta'], errors='coerce')
    df_btc['Baixa'] = pd.to_numeric(df_btc['Baixa'], errors='coerce')
    df_btc['Variação'] = pd.to_numeric(df_btc['Variação'], errors='coerce')
    df_btc['% Variação'] = pd.to_numeric(df_btc['% Variação'], errors='coerce')
    df_btc['Bid'] = pd.to_numeric(df_btc['Bid'], errors='coerce')
    df_btc['Ask'] = pd.to_numeric(df_btc['Ask'], errors='coerce')

    df_geral = pd.concat([df_usd, df_eur, df_btc], ignore_index=True)
    df_geral = df_geral.dropna(subset=['% Variação'])
    df_geral['Orig/Conv'] = df_geral['Origem'] + '/' + df_geral['Convertido Para']

    #Montando Gráfico com a % das Variações

    plt.figure(figsize=(4, 4))
    plt.bar(df_geral['Orig/Conv'], df_geral['% Variação'], color='blue')

    for i, value in enumerate(df_geral['% Variação']):
        if value >= 0:
            plt.text(i, value - 0.2, f'{value:.2f}%', ha='center', va='bottom', color='white')
        else:
            plt.text(i, value + 0.40, f'{value:.2f}%', ha='center', va='top')

    plt.xlabel('Moeda')
    plt.ylabel('Variação')
    plt.title('Maiores Variações das Moedas')
    plt.xticks(rotation=45, ha='right')
    plt.yticks([])
    plt.tight_layout()
    plt.savefig('grafico_maiores_variacoes.png')

    nome_graf_var = 'grafico_maiores_variacoes.png'
    caminho_grafico = os.path.join(diretorio, nome_graf_var)

    #Criando as variáveis com as informações para montar o Report
    assunto = f"Report Financeiro - {dia_atual}"
   
    
    #Valor Atual
    usd_atual = ((df_usd['Bid'] + df_usd['Ask'])/2).values[0]
    eur_atual = ((df_eur['Bid'] + df_eur['Ask'])/2).values[0]
    btc_atual = ((df_btc['Bid'] + df_btc['Ask'])/2).values[0]

    #Variação
    usd_var = df_usd['% Variação'].values[0]
    eur_var = df_eur['% Variação'].values[0]
    btc_var = df_btc['% Variação'].values[0]

    #Alta do Dia
    usd_alt = df_usd['Alta'].values[0]
    eur_alt = df_eur['Alta'].values[0]
    btc_alt = df_btc['Alta'].values[0]

    #Baixa do Dia
    usd_baixa = df_usd['Baixa'].values[0]
    eur_baixa = df_eur['Baixa'].values[0]
    btc_baixa = df_btc['Baixa'].values[0]
    
    #Enviando as variáveis para a função de criar o Report
    criar_pdf(assunto, usd_atual, eur_atual, btc_atual, usd_var, eur_var, btc_var, usd_alt, eur_alt, btc_alt, usd_baixa, eur_baixa, btc_baixa, caminho_grafico)

    if os.path.exists(nome_graf_var):
        os.remove(nome_graf_var)

principal()


