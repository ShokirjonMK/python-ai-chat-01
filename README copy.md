# python-ai-chat-01



ollama download:
 
```docker run -d --name ollama -p 11434:11434 ollama/ollama```


# llama3 ni ishga tushurish
```docker exec -it ollama bash```

```ollama run llama3```


# gemma ni ishga tushurish
```docker exec -it ollama bash```

```ollama run gemma:2b```

```ollama run gemma:7b```


# gemma How to use from Ollama

```huggingface-cli login```

```ollama run hf.co/google/gemma-2b-it```


# To'xtatish va o'chirish:

```docker stop ollama``` 

```docker rm ollama```
