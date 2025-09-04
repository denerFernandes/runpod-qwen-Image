# Qwen-Image RunPod Serverless

[English](#english) | [Polski](#polski) | [Português](#português) | [Español](#español)

---

## English

A RunPod serverless implementation for the Qwen-Image model, enabling high-quality image generation with advanced text rendering capabilities.

### 🚀 Features

- **High-Quality Image Generation**: Uses Qwen-Image model for realistic image creation
- **Text Rendering**: Capable of rendering text in multiple languages (English, Chinese, etc.)
- **Multiple Aspect Ratios**: Support for different aspect ratios (1:1, 16:9, 9:16, 4:3, 3:4)
- **Custom Dimensions**: Allows specifying width and height directly
- **Flexible API**: Configurable parameters for fine-tuned generation control
- **GPU Optimization**: Automatic CUDA detection for better performance
- **Pre-downloaded Models**: Models downloaded during image build for fast initialization
- **Model Caching**: Single model loading for multiple requests
- **Error Handling**: Structured responses with appropriate error codes

### 📁 Project Structure

```
qwen-image-runpod/
├── handler.py          # Main serverless logic
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
├── download_model.py   # Script to download models during build
├── runpod.toml        # RunPod configuration
├── README.md          # Documentation
├── test_example.py    # Local testing script
├── test_input.json    # Test input examples
└── .gitignore         # Git ignored files
```

### 🔧 Performance Optimization

#### Model Download During Build

To optimize initialization time, models are downloaded during Docker image construction:

- **`download_model.py`**: Script that downloads Qwen-Image model during build
- **Local Cache**: Models stored in `/app/cache` within container
- **Fast Initialization**: Handler loads models from local cache, avoiding downloads during execution
- **Fallback**: If cache fails, system automatically downloads online

Results in:
- ⚡ Significantly reduced cold start time
- 🚀 Faster first request
- 💾 Efficient network resource usage

### 🚀 RunPod Deployment

#### Using RunPod CLI

```bash
# Install RunPod CLI
pip install runpod

# Deploy the serverless function
runpod deploy
```

#### Manual Configuration

1. Create a new serverless endpoint on RunPod
2. Upload the project files
3. Set the handler to `handler.py`
4. Configure GPU resources (recommended: RTX 4090 or better)

### 📝 API Usage

#### Input Parameters

```json
{
  "input": {
    "prompt": "A beautiful sunset over mountains",
    "aspect_ratio": "16:9",
    "width": 1664,
    "height": 928,
    "num_inference_steps": 50,
    "true_cfg_scale": 4.0,
    "negative_prompt": "blurry, low quality",
    "seed": 42,
    "language": "en"
  }
}
```

#### Parameters

- **prompt** (required): Text description for image generation
- **aspect_ratio** (optional): Image aspect ratio ("1:1", "16:9", "9:16", "4:3", "3:4")
- **width** (optional): Custom image width in pixels
- **height** (optional): Custom image height in pixels
- **num_inference_steps** (optional): Number of denoising steps (default: 50)
- **true_cfg_scale** (optional): CFG scale for prompt adherence (default: 4.0)
- **negative_prompt** (optional): What to avoid in the image
- **seed** (optional): Random seed for reproducible results
- **language** (optional): Prompt language ("en", "zh")

*Note: If `width` and `height` are specified, `aspect_ratio` is ignored.*

#### Output

```json
{
  "image_base64": "iVBORw0KGgoAAAANSUhEUgAA...",
  "width": 1664,
  "height": 928,
  "seed": 42
}
```

### 💡 Usage Examples

#### Example 1: Basic Generation
```json
{
  "input": {
    "prompt": "A serene lake with mountains in the background",
    "aspect_ratio": "16:9"
  }
}
```

#### Example 2: Chinese Text
```json
{
  "input": {
    "prompt": "一个现代咖啡店，门口有霓虹灯标志",
    "language": "zh",
    "aspect_ratio": "1:1"
  }
}
```

#### Example 3: Custom Dimensions
```json
{
  "input": {
    "prompt": "A panoramic landscape with mountains and rivers",
    "width": 2048,
    "height": 1024,
    "num_inference_steps": 50
  }
}
```

### 🔧 Local Testing

Run the test script:

```bash
python test_example.py
```

### 📋 Requirements

- **GPU**: NVIDIA GPU with at least 8GB VRAM (recommended: RTX 4090)
- **Memory**: 16GB+ RAM
- **Storage**: 20GB+ available space

---

## Polski

Implementacja RunPod serverless dla modelu Qwen-Image, umożliwiająca generowanie wysokiej jakości obrazów z zaawansowanymi możliwościami renderowania tekstu.

### 🚀 Funkcje

- **Generowanie Obrazów Wysokiej Jakości**: Wykorzystuje model Qwen-Image do tworzenia realistycznych obrazów
- **Renderowanie Tekstu**: Możliwość renderowania tekstu w wielu językach (angielski, chiński, itp.)
- **Różne Proporcje**: Wsparcie dla różnych proporcji obrazu (1:1, 16:9, 9:16, 4:3, 3:4)
- **Niestandardowe Wymiary**: Możliwość bezpośredniego określenia szerokości i wysokości
- **Elastyczne API**: Konfigurowalne parametry dla precyzyjnej kontroli generowania
- **Optymalizacja GPU**: Automatyczne wykrywanie CUDA dla lepszej wydajności
- **Wstępnie Pobrane Modele**: Modele pobierane podczas budowy obrazu dla szybkiej inicjalizacji
- **Buforowanie Modeli**: Jednorazowe ładowanie modelu dla wielu żądań
- **Obsługa Błędów**: Strukturalne odpowiedzi z odpowiednimi kodami błędów

### 🚀 Wdrożenie RunPod

#### Używając RunPod CLI

```bash
# Zainstaluj RunPod CLI
pip install runpod

# Wdróż funkcję serverless
runpod deploy
```

### 📝 Użycie API

#### Parametry Wejściowe

```json
{
  "input": {
    "prompt": "Piękny zachód słońca nad górami",
    "aspect_ratio": "16:9",
    "num_inference_steps": 50,
    "seed": 42
  }
}
```

---

## Português

Uma implementação RunPod serverless para o modelo Qwen-Image, permitindo geração de imagens de alta qualidade com capacidades avançadas de renderização de texto.

### 🚀 Características

- **Geração de Imagens de Alta Qualidade**: Utiliza o modelo Qwen-Image para criar imagens realistas
- **Renderização de Texto**: Capaz de renderizar texto em múltiplos idiomas (inglês, chinês, etc.)
- **Múltiplas Proporções**: Suporte para diferentes aspect ratios (1:1, 16:9, 9:16, 4:3, 3:4)
- **Dimensões Customizadas**: Permite especificar width e height diretamente
- **API Flexível**: Parâmetros configuráveis para controle fino da geração
- **Otimização para GPU**: Detecção automática de CUDA para melhor performance
- **Modelos Pré-baixados**: Download dos modelos durante o build da imagem para inicialização rápida
- **Caching de Modelo**: Carregamento único do modelo para múltiplas requisições
- **Tratamento de Erros**: Respostas estruturadas com códigos de erro apropriados

### 🚀 Deployment no RunPod

#### Usando RunPod CLI

```bash
# Instalar RunPod CLI
pip install runpod

# Fazer deploy da função serverless
runpod deploy
```

### 📝 Uso da API

#### Parâmetros de Entrada

```json
{
  "input": {
    "prompt": "Um belo pôr do sol sobre as montanhas",
    "aspect_ratio": "16:9",
    "num_inference_steps": 50,
    "seed": 42
  }
}
```

---

## Español

Una implementación RunPod serverless para el modelo Qwen-Image, que permite la generación de imágenes de alta calidad con capacidades avanzadas de renderizado de texto.

### 🚀 Características

- **Generación de Imágenes de Alta Calidad**: Utiliza el modelo Qwen-Image para crear imágenes realistas
- **Renderizado de Texto**: Capaz de renderizar texto en múltiples idiomas (inglés, chino, etc.)
- **Múltiples Proporciones**: Soporte para diferentes relaciones de aspecto (1:1, 16:9, 9:16, 4:3, 3:4)
- **Dimensiones Personalizadas**: Permite especificar ancho y alto directamente
- **API Flexible**: Parámetros configurables para control fino de la generación
- **Optimización GPU**: Detección automática de CUDA para mejor rendimiento
- **Modelos Pre-descargados**: Descarga de modelos durante la construcción de imagen para inicialización rápida
- **Caché de Modelos**: Carga única del modelo para múltiples solicitudes
- **Manejo de Errores**: Respuestas estructuradas con códigos de error apropiados

### 🚀 Despliegue en RunPod

#### Usando RunPod CLI

```bash
# Instalar RunPod CLI
pip install runpod

# Desplegar la función serverless
runpod deploy
```

### 📝 Uso de la API

#### Parámetros de Entrada

```json
{
  "input": {
    "prompt": "Una hermosa puesta de sol sobre las montañas",
    "aspect_ratio": "16:9",
    "num_inference_steps": 50,
    "seed": 42
  }
}
```

---

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.