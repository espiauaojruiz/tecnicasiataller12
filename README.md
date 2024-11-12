## Taller 2
Para este taller se plantea una aplicación chatbot que permita a los usuarios obtener respuestas sobre inquietudes relacionadas con sus contratos de arrendamiento, para esta app se hace uso del modelo ```gpt-4o```, ```Chroma DB``` y la tecnica RAG que permita obtener información relevante de los diferentes contratos de arrendamiento.

En un navegador web se cargará la aplicación, en la parte izquierda se visualizará una barra vertical con un componente que permita la carga de documentos PDF al sistema,  y en la parte derecha el componente para poder realizar preguntas y obtenber respuestas (chatbot).

### Estructura del proyecto
```
/Proyecto
│
├──- app.py
│
├──- database.py
│
├──- document.py
│
├──- database.py
│
└── requirements.txt
```

### Requisitos
* Python 3.8+
* En el diractorio raíz del proyecto crear el archivo ```.env``` en el cual se deberá especificar el API key con la clave ```OPENAI_API_KEY```
* Instalación de las dependencias, desde el diractorio raíz del proyecto ejecutar el comando ```pip install -r requirements.txt```

### Uso
* Desde el diractorio raíz del proyecto ejecutar el comando ```streamlit run app.py```
