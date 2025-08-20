import { AssetsConfig } from '@capacitor/assets';

const config: AssetsConfig = {
  icon: {
    source: 'static/favicon.svg',
    backgroundColor: '#0d6efd',
    resizeMode: 'contain',
    platform: {
      android: {
        targetDir: 'mipmap',
        icon: {
          foreground: 'static/favicon.svg',
          background: '#0d6efd',
          adaptiveForeground: 'static/favicon.svg',
          adaptiveBackground: '#0d6efd'
        }
      }
    }
  },
  splash: {
    source: 'static/favicon.svg',
    backgroundColor: '#0d6efd',
    resizeMode: 'contain',
    platform: {
      android: {
        backgroundColor: '#0d6efd',
        resize: 'contain',
        dark: {
          backgroundColor: '#ffffff'
        }
      }
    }
  }
};

export default config;
