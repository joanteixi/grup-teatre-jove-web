// @ts-check
import { defineConfig } from 'astro/config';

import react from '@astrojs/react';

// https://astro.build/config
export default defineConfig({
  // PLACEHOLDER: canvia-ho pel domini definitiu abans de publicar.
  // Serveix per als enllaços canònics, el sitemap i les previsualitzacions
  // quan es comparteix la web per WhatsApp o xarxes socials.
  site: 'https://www.grupteatrejove.cat',
  integrations: [react()],
});