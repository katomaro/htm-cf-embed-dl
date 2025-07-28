import sys
import logging
from pathlib import Path
from yt_dlp import YoutubeDL


logging.getLogger('yt_dlp').setLevel(logging.ERROR)

# Headers para todos os downloads
HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,pt;q=0.8',
    'cache-control': 'no-cache',
    'origin': 'https://cf-embed.play.hotmart.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://cf-embed.play.hotmart.com/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}

class ProgressLogger:
    def __init__(self):
        self.last_percent = 0
        self.last_speed = 0
        self.start_time = None
        import time
        self.time = time
    
    def debug(self, msg):
        pass
    
    def warning(self, msg):
        pass
    
    def error(self, msg):
        print(f"❌ Erro: {msg}")
    
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            speed = d.get('speed', 0)
            
            if total > 0:
                percent = (downloaded / total * 100)
                
                if percent - self.last_percent >= 2 or speed != self.last_speed:
                    speed_str = f"{speed/1024/1024:.1f} MB/s" if speed else "calculando..."
                    eta = d.get('eta', 0)
                    if eta and eta > 0:
                        eta_minutes = int(eta // 60)
                        eta_seconds = int(eta % 60)
                        eta_str = f"{eta_minutes:02d}:{eta_seconds:02d}"
                    else:
                        eta_str = "calculando..."
                    
                    bar_length = 30
                    filled_length = int(bar_length * percent / 100)
                    bar = '█' * filled_length + '░' * (bar_length - filled_length)
                    
                    print(f"\r📥 {bar} {percent:.1f}% | {speed_str} | ETA: {eta_str}", end='', flush=True)
                    
                    self.last_percent = percent
                    self.last_speed = speed
                    
        elif d['status'] == 'finished':
            print(f"\n✅ Download finalizado!")
            self.last_percent = 0
            self.last_speed = 0
        elif d['status'] == 'error':
            print(f"\n❌ Falha durante o download.")

def get_concurrent_fragments():
    """Get the number of concurrent fragments from user input."""
    while True:
        try:
            fragments_input = input("Entre o número de segmentos concorrentes (padrão 6): ").strip()
            if not fragments_input:
                return 6
            fragments = int(fragments_input)
            if fragments < 1:
                print("Erro: O número de segmentos concorrentes deve ser pelo menos 1")
                continue
            if fragments > 32:
                print("Aviso: um número muito alto de segmentos concorrentes pode causar problemas")
            return fragments
        except ValueError:
            print("Erro: Por favor, entre um número válido")
        except KeyboardInterrupt:
            print("\nctrl+c pressionado, saindo...")
            sys.exit(0)

def get_save_folder():
    """Get the save folder from user input."""
    while True:
        try:
            folder_input = input("📁 Entre o caminho da pasta de salvamento: ").strip()
            if not folder_input:
                print("❌ Erro: a pasta de salvamento não pode ser vazia (Digite algo)")
                continue
            
            save_path = Path(folder_input)
            
            if not save_path.exists():
                try:
                    save_path.mkdir(parents=True, exist_ok=True)
                    print(f"📂 Criada a árvore de diretórios: {save_path}")
                except Exception as e:
                    print(f"❌ Erro ao criar a árvore de diretórios: {e}")
                    continue
            
            if not save_path.is_dir():
                print("❌ Erro: o caminho existe mas não é uma pasta")
                continue
            
            print(f"   ✅ Pasta configurada: {save_path}")
            return save_path
            
        except KeyboardInterrupt:
            print("\n👋 ctrl+c pressionado, saindo...")
            sys.exit(0)

def get_video_info():
    """Get video name and URL from user input."""
    try:
        print("\n" + "🎬" + "═"*48 + "🎬")
        video_name = input("🎥 Digite o nome do vídeo (sem extensão): ").strip()
        if not video_name:
            print("❌ Erro: o nome do vídeo não pode ser vazio")
            return None, None
        
        video_url = input("🔗 Digite a URL do master-pkg da Hotmart (https://vod-akm.play.hotmart.com/video/XXXXXXXX/hls/master-pkg-t-XXXXXX): ").strip()
        if not video_url:
            print("❌ Erro: a URL não pode ser vazia")
            return None, None
        
        print(f"   📝 Nome: {video_name}")
        print(f"   🔗 URL: {video_url[:50]}..." if len(video_url) > 50 else f"   🔗 URL: {video_url}")
            
        return video_name, video_url
        
    except KeyboardInterrupt:
        print("\n👋 Saindo...")
        sys.exit(0)

def download_video(url, save_path, video_name, concurrent_fragments):
    """Download a video using yt-dlp with the specified parameters."""
    
    outtmpl = str(save_path / f"{video_name}.%(ext)s")
    
    logger = ProgressLogger()
    
    ydl_opts = {
        'outtmpl': outtmpl,
        'http_headers': HEADERS,
        'allow_unplayable_formats': True,
        'nocheckcertificate': True,
        'progress_hooks': [logger.progress_hook],
        'logger': logger,
        'concurrent_fragment_downloads': concurrent_fragments,
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        print(f"\n🎬 Iniciando o download...")
        print(f"   🔗 URL: {url}")
        print(f"   📁 Salvando em: {save_path}")
        print(f"   🎥 Título do vídeo: {video_name}")
        print(f"   ⚡ Segmentos simultâneos: {concurrent_fragments}")
        print("─" * 60)
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("✅ Download concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o download: {e}")
        return False

def main():
    print("🚀 === Hotmart Cloudfront embed Downloader ===")
    print("💡 Pressione ctrl+c a qualquer momento para sair")
    
    try:
        concurrent_fragments = get_concurrent_fragments()
        save_folder = get_save_folder()
        
        print(f"\n⚙️  Configuração:")
        print(f"   📊 Segmentos simultâneos: {concurrent_fragments}")
        print(f"   📁 Caminho de download: {save_folder}")
        print(f"\n🔄 Iniciando o Loop de download de vídeos...")
        
        while True:
            video_name, video_url = get_video_info()
            
            if video_name is None or video_url is None:
                print("⚠️  Pulando por input inválida...")
                continue
            
            success = download_video(video_url, save_folder, video_name, concurrent_fragments)
            
            if success:
                print("🎉 Pronto para o próximo download!")
            else:
                print("❌ Ish, o download falhou. Tente novamente com outros parâmetros.")
                
    except KeyboardInterrupt:
        print("\n\n👋 Saindo!")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Erro inesperado: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
