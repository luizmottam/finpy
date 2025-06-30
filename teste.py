<<<<<<< HEAD
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


=======
from pathlib import Path
from fpdf import FPDF

# Criando o conteúdo do PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

title = "Escolha de Tecnologias para Projeto de Tópicos de Dados"
pdf.set_font("Arial", 'B', 14)
pdf.multi_cell(0, 10, title)
pdf.set_font("Arial", size=12)

sections = {
    "🔁 Sincronização e Processamento entre os BDs (ETL/ELT + Orquestração)": [
        "Apache NiFi – Pipeline visual, compatível com Kafka, usado para orquestrar fluxos entre sistemas.",
        "Apache Airflow – Agendamento e orquestração de workflows com integração via operadores para Kafka, bancos e Spark.",
        "dbt (Data Build Tool) – Utilizado para transformar dados no data warehouse com SQL, integrado com Airflow e Kafka.",
        "StreamSets – Pipeline de dados com integração com Kafka e suporte a diferentes bancos.",
        "Talend – Plataforma ETL com conector nativo para Kafka, bancos relacionais e data lakes."
    ],
    "➡️ Envio para o Banco Transacional": [
        "Kafka Connect (com JDBC Sink Connector) – Envia dados estruturados diretamente do Kafka para bancos relacionais como PostgreSQL, MySQL etc.",
        "Debezium – Excelente para CDC e sincronização entre bancos relacionais via Kafka.",
        "NiFi – Também pode ser usado para enviar dados do tópico para o banco transacional via JDBC.",
    ],
    "📊 Envio para o Banco Analítico": [
        "Kafka Connect (com conector para BigQuery, ClickHouse, Snowflake, etc.) – Alta compatibilidade com bancos analíticos.",
        "Apache Spark Streaming – Transforma dados em tempo real e envia para o banco analítico.",
        "Apache Flink – Alternativa ao Spark para ETL em tempo real, totalmente compatível com Kafka.",
        "dbt – Para transformar dados no destino analítico após ingestão.",
    ],
    "🧽 Preparação dos dados para consumo (transformações)": [
        "Apache Spark – Framework robusto para transformação de dados em lote ou streaming.",
        "Apache Flink – Ideal para transformações com baixa latência e janelas temporais.",
        "ksqlDB – SQL para streams Kafka, útil para transformação e enriquecimento em tempo real.",
        "Kafka Streams – Biblioteca Java para transformação de dados direto no Kafka.",
        "Airbyte – Ferramenta de extração e carregamento com suporte a Kafka e transformação opcional via dbt.",
    ]
}

for section, tools in sections.items():
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, section, ln=True)
    pdf.set_font("Arial", size=11)
    for tool in tools:
        pdf.multi_cell(0, 8, f"- {tool}")
    pdf.ln()

# Salvando o PDF
output_path = "./Tecnologias_Topicos_de_Dados_Atualizado.pdf"
pdf.output(output_path)
>>>>>>> b1f1758822f23d1ef25c6c4414fbd5b7d3a6ccc2
