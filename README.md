# WikiWise Chat Application

Welcome to WikiWise, an innovative chat application that bridges the gap between users and the vast knowledge of Wikipedia. Hosted at [wikiwise.streamlit.app](https://wikiwise.streamlit.app), this app is designed to provide an interactive and engaging way to explore topics and find answers directly from Wikipedia in a conversational manner. Whether you're curious about historical events, scientific concepts, or any topic imaginable, WikiWise is here to guide you through the wealth of information available on Wikipedia.

## Features

- **Interactive Chat Interface**: Engage in a conversation with WikiWise as if you were chatting with a friend. Ask questions and get responses that are informative and easy to understand.
- **Dynamic Topic Selection**: Enter any topic of your interest, and the app will fetch the relevant Wikipedia URL to source its answers from. 
- **Smart Question Answering**: Leveraging advanced AI techniques, WikiWise parses your questions and retrieves answers from the Wikipedia page related to your selected topic. The app intelligently formats responses to fit the chat interface, making information consumption seamless.
- **PDF Generation**: For every topic queried, the app creates a PDF version of the relevant Wikipedia page, making it easy to save, share, or refer to the information offline.

## How It Works - Behind the Scenes

WikiWise is built using a combination of cutting-edge technologies and libraries to deliver a seamless and responsive user experience. Here's a brief overview of the core components:

- **Streamlit**: The front-end of the app is built with Streamlit, which allows for rapid development of data apps with a focus on machine learning and data science.
- **Python**: The back-end logic, including the chat interface and Wikipedia data retrieval, is implemented in Python, making use of its robust ecosystem.
- **LangChain**: For understanding and generating responses, WikiWise leverages LangChain, a library for building language model applications, enabling sophisticated question answering capabilities.
- **OpenAI's GPT Models**: At the heart of the question-answering mechanism is OpenAI's powerful generative models, which are used to parse questions and generate accurate and relevant answers.
- **Supabase**: For storage needs, including storing PDF versions of Wikipedia pages, WikiWise utilizes Supabase, an open-source Firebase alternative.
- **ConvertAPI**: This service is used to convert Wikipedia pages into PDF format, facilitating the PDF generation feature of the app.

## Contribute

If you have suggestions for improvements or new features, feel free to reach out or submit a pull request on our GitHub repository.

## License

WikiWise is released under the MIT License. This license permits free use, modification, and distribution of the software, making it an excellent choice for open-source projects. For more details, see the [LICENSE](LICENSE.md) file in the project repository.

## Disclaimer

WikiWise is powered by Wikipedia content, and while it strives to provide accurate and up-to-date information, I encourage users to refer directly to Wikipedia for critical research or information verification.

Enjoy your journey through the world of knowledge with WikiWise!
