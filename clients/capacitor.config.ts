import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'org.autostream.sama',
  appName: 'Sama Calculator',
  webDir: 'build',
  server: {
    androidScheme: 'https',
    cleartext: true,
  },
  plugins: {
    CapacitorHttp: {
      enabled: true
    }
  }
}

export default config;
