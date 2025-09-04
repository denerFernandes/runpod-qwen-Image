#!/usr/bin/env python3
"""
Exemplo de teste para a função serverless Qwen-Image
Este arquivo demonstra como usar a função localmente para testes
"""

import json
import base64
from PIL import Image
from io import BytesIO

# Importar a função do handler (para teste local)
try:
    from handler import generate_image
except ImportError:
    print("Erro: Não foi possível importar o handler. Certifique-se de que está no diretório correto.")
    exit(1)

def save_base64_image(base64_string, filename):
    """Salva uma imagem base64 como arquivo"""
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    image.save(filename)
    print(f"Imagem salva como: {filename}")

def test_basic_generation():
    """Teste básico de geração de imagem"""
    print("\n=== Teste 1: Geração Básica ===")
    
    job = {
        "input": {
            "prompt": "A beautiful sunset over mountains with a lake reflection",
            "aspect_ratio": "16:9",
            "num_inference_steps": 30,  # Reduzido para teste mais rápido
            "seed": 42
        }
    }
    
    print(f"Prompt: {job['input']['prompt']}")
    result = generate_image(job)
    
    if "error" in result:
        print(f"Erro: {result['error']}")
        return False
    
    print(f"Dimensões: {result['width']}x{result['height']}")
    save_base64_image(result["image"], "test_basic.png")
    return True

def test_chinese_text():
    """Teste com texto em chinês"""
    print("\n=== Teste 2: Texto em Chinês ===")
    
    job = {
        "input": {
            "prompt": "一个现代咖啡店，门口有霓虹灯标志写着'欢迎光临'，旁边有美丽的花朵",
            "language": "zh",
            "aspect_ratio": "1:1",
            "num_inference_steps": 30,
            "seed": 123
        }
    }
    
    print(f"Prompt: {job['input']['prompt']}")
    result = generate_image(job)
    
    if "error" in result:
        print(f"Erro: {result['error']}")
        return False
    
    print(f"Dimensões: {result['width']}x{result['height']}")
    save_base64_image(result["image"], "test_chinese.png")
    return True

def test_text_rendering():
    """Teste específico para renderização de texto"""
    print("\n=== Teste 3: Renderização de Texto ===")
    
    job = {
        "input": {
            "prompt": 'A coffee shop entrance features a chalkboard sign reading "Qwen Coffee 😊 $2 per cup," with a neon light beside it displaying "通义千问"',
            "aspect_ratio": "4:3",
            "num_inference_steps": 40,
            "true_cfg_scale": 5.0,
            "seed": 456
        }
    }
    
    print(f"Prompt: {job['input']['prompt']}")
    result = generate_image(job)
    
    if "error" in result:
        print(f"Erro: {result['error']}")
        return False
    
    print(f"Dimensões: {result['width']}x{result['height']}")
    save_base64_image(result["image"], "test_text_rendering.png")
    return True

def test_portrait_mode():
    """Teste em modo retrato"""
    print("\n=== Teste 4: Modo Retrato ===")
    
    job = {
        "input": {
            "prompt": "A tall modern skyscraper reaching into the clouds, architectural photography",
            "aspect_ratio": "9:16",
            "num_inference_steps": 35,
            "negative_prompt": "blurry, low quality, distorted",
            "seed": 789
        }
    }
    
    print(f"Prompt: {job['input']['prompt']}")
    result = generate_image(job)
    
    if "error" in result:
        print(f"Erro: {result['error']}")
        return False
    
    print(f"Dimensões: {result['width']}x{result['height']}")
    save_base64_image(result["image"], "test_portrait.png")
    return True

def test_custom_dimensions():
    """Teste com dimensões customizadas"""
    print("\n=== Teste 5: Dimensões Customizadas ===")
    
    job = {
        "input": {
            "prompt": "A panoramic landscape with mountains and rivers, ultra wide view",
            "width": 2048,
            "height": 1024,
            "num_inference_steps": 40,
            "true_cfg_scale": 4.5,
            "seed": 999
        }
    }
    
    print(f"Prompt: {job['input']['prompt']}")
    print(f"Dimensões customizadas: {job['input']['width']}x{job['input']['height']}")
    result = generate_image(job)
    
    if "error" in result:
        print(f"Erro: {result['error']}")
        return False
    
    print(f"Dimensões resultantes: {result['width']}x{result['height']}")
    save_base64_image(result["image"], "test_custom_dimensions.png")
    return True

def main():
    """Executa todos os testes"""
    print("Iniciando testes da função Qwen-Image Serverless...")
    print("Nota: Os testes podem demorar alguns minutos dependendo do hardware.")
    
    tests = [
        test_basic_generation,
        test_chinese_text,
        test_text_rendering,
        test_portrait_mode,
        test_custom_dimensions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
                print("✅ Teste passou!")
            else:
                print("❌ Teste falhou!")
        except Exception as e:
            print(f"❌ Teste falhou com exceção: {e}")
    
    print(f"\n=== Resumo dos Testes ===")
    print(f"Testes passaram: {passed}/{total}")
    print(f"Taxa de sucesso: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 Todos os testes passaram! O serverless está funcionando corretamente.")
    else:
        print("⚠️ Alguns testes falharam. Verifique os logs para mais detalhes.")

if __name__ == "__main__":
    main()