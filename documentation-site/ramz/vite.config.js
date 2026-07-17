import { defineConfig } from 'vite';
import plugin from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [plugin()],
    base: '/RAMZ/',
    server: {
        port: 57964,
    }
});