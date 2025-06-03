import { Route, RouteCategory } from '../types/route';

export const routeDetails: Record<string, Route> = {
  petersburg: {
    id: "petersburg",
    title: "Романтический Петербург",
    description: "Эрмитаж, Невский проспект, прогулки по рекам.",
    category: "culture" as RouteCategory,
    details: "Подробное описание маршрута по Санкт-Петербургу...",
    checklist: [
      {
        title: "Эрмитаж",
        description: "Посещение главного музея России",
        photo: "/images/hermitage.jpg"
      },
      {
        title: "Невский проспект",
        description: "Прогулка по главной улице города",
        photo: "/images/nevsky.jpg"
      }
    ]
  },
  "zolotoe-kolco": {
    id: "zolotoe-kolco",
    title: "Золотое кольцо России",
    description: "Владимир, Суздаль, Ростов Великий — история и архитектура.",
    category: "culture" as RouteCategory,
    details: "Подробное описание маршрута по Золотому кольцу...",
    checklist: [
      {
        title: "Владимир",
        description: "Древний город с богатой историей",
        photo: "/images/vladimir.jpg"
      },
      {
        title: "Суздаль",
        description: "Город-музей под открытым небом",
        photo: "/images/suzdal.jpg"
      }
    ]
  },
  kavkaz: {
    id: "kavkaz",
    title: "Кавказские горы",
    description: "Домбай, Эльбрус, горные тропы и горячие источники.",
    category: "nature" as RouteCategory,
    details: "Подробное описание маршрута по Кавказу...",
    checklist: [
      {
        title: "Домбай",
        description: "Горнолыжный курорт и природные красоты",
        photo: "/images/dombay.jpg"
      },
      {
        title: "Эльбрус",
        description: "Высочайшая точка России",
        photo: "/images/elbrus.jpg"
      }
    ]
  },
  sochi: {
    id: "sochi",
    title: "Сочи и Черноморское побережье",
    description: "Пляжи, горы и современный курортный отдых.",
    category: "relax" as RouteCategory,
    details: "Подробное описание маршрута по Сочи...",
    checklist: [
      {
        title: "Красная Поляна",
        description: "Горнолыжный курорт и природные красоты",
        photo: "/images/krasnaya-polyana.jpg"
      },
      {
        title: "Пляжи Сочи",
        description: "Отдых на Черноморском побережье",
        photo: "/images/sochi-beach.jpg"
      }
    ]
  },
  karelia: {
    id: "karelia",
    title: "Карелия — земля озёр",
    description: "Природные красоты, леса и водопады.",
    category: "nature" as RouteCategory,
    details: "Подробное описание маршрута по Карелии...",
    checklist: [
      {
        title: "Кижи",
        description: "Музей-заповедник деревянного зодчества",
        photo: "/images/kizhi.jpg"
      },
      {
        title: "Рускеала",
        description: "Мраморный каньон и водопады",
        photo: "/images/ruskeala.jpg"
      }
    ]
  },
  altai: {
    id: "altai",
    title: "Алтай",
    description: "Горы, чистые реки, древние петроглифы.",
    category: "adventure" as RouteCategory,
    details: "Подробное описание маршрута по Алтаю...",
    checklist: [
      {
        title: "Телецкое озеро",
        description: "Жемчужина Алтая",
        photo: "/images/teletskoye.jpg"
      },
      {
        title: "Чуйский тракт",
        description: "Одна из красивейших дорог мира",
        photo: "/images/chuisky-tract.jpg"
      }
    ]
  },
  urals: {
    id: "urals",
    title: "Уральские горы",
    description: "Свердловск, Пермь, красивые горные пейзажи.",
    category: "nature" as RouteCategory,
    details: "Урал — это одно из самых красивых и разнообразных мест в России, с живописными горами и культурными памятниками.",
    checklist: [
      {
        title: "Гора Ямантау",
        description: "Популярное место для походов и пикников.",
        photo: "/images/yamantau.jpg"
      },
      {
        title: "Каменные реки",
        description: "Уникальные каменные образования в Урале.",
        photo: "/images/stone_rivers.jpg"
      }
    ]
  },
  volga: {
    id: "volga",
    title: "Волга",
    description: "Волгоград, Казань, исторические города и природа.",
    category: "culture" as RouteCategory,
    details: "Волга — величественная река с множеством городов, культурных и природных достопримечательностей.",
    checklist: [
      {
        title: "Волгоградская набережная",
        description: "Прекрасная прогулочная зона на реке.",
        photo: "/images/volgograd.jpg"
      },
      {
        title: "Казанский кремль",
        description: "Уникальная крепость в Казани.",
        photo: "/images/kazan_kremlin.jpg"
      }
    ]
  },
  siberia: {
    id: "siberia",
    title: "Сибирь",
    description: "Томск, Новосибирск, дикая природа.",
    category: "nature" as RouteCategory,
    details: "Сибирь — это огромное пространство с природой, которую не встречаешь нигде в мире.",
    checklist: [
      {
        title: "Ледяные пещеры",
        description: "Известные пещеры в Сибири.",
        photo: "/images/ice_caves.jpg"
      },
      {
        title: "Байкал",
        description: "Озеро Байкал — одно из самых глубоких озёр в мире.",
        photo: "/images/baikal.jpg"
      }
    ]
  },
  "kamchatka-vulkan": {
    id: "kamchatka-vulkan",
    title: "Вулканы Камчатки",
    description: "Земля огня, горячие источники.",
    category: "adventure" as RouteCategory,
    details: "Камчатка славится своими активными вулканами и природными горячими источниками.",
    checklist: [
      {
        title: "Гора Вулкан Шивелуч",
        description: "Активный вулкан Камчатки.",
        photo: "/images/shiveluch.jpg"
      },
      {
        title: "Гейзеры в Долине Гейзеров",
        description: "Долина, полная вулканических гейзеров.",
        photo: "/images/geysers.jpg"
      }
    ]
  }
};

