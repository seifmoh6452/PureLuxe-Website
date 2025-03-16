import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
  en: {
    translation: {
      'PureLuxe - Ramadan Kareem': 'PureLuxe - Ramadan Kareem',
      'Ramadan Kareem': 'Ramadan Kareem',
      'Experience the essence of pure luxury this Ramadan': 'Experience the essence of pure luxury this Ramadan',
      'Days': 'Days',
      'Hours': 'Hours',
      'Minutes': 'Minutes',
      'Seconds': 'Seconds',
      'Until the end of Ramadan': 'Until the end of Ramadan',
      'One Product, Double Benefits': 'One Product, Double Benefits',
      'Experience the perfect blend of nature and science': 'Experience the perfect blend of nature and science',
      'What Our Customers Say': 'What Our Customers Say'
    }
  },
  ar: {
    translation: {
      'PureLuxe - Ramadan Kareem': 'بيور لوكس - رمضان كريم',
      'Ramadan Kareem': 'رمضان كريم',
      'Experience the essence of pure luxury this Ramadan': 'اختبر جوهر الفخامة النقية هذا الرمضان',
      'Days': 'أيام',
      'Hours': 'ساعات',
      'Minutes': 'دقائق',
      'Seconds': 'ثواني',
      'Until the end of Ramadan': 'حتى نهاية رمضان',
      'One Product, Double Benefits': 'منتج واحد، فوائد مضاعفة',
      'Experience the perfect blend of nature and science': 'اختبر المزيج المثالي بين الطبيعة والعلم',
      'What Our Customers Say': 'ماذا يقول عملاؤنا'
    }
  }
};

i18n
  .use(initReactI18next)
  .init({
    resources,
    lng: 'en',
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;
