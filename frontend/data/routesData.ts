export type ChecklistItem = {
  title: string;
  description: string;
  photo: string;
};

export const routeDetails = {
  petersburg: {
    title: "Романтический Петербург",
    description: "Эрмитаж, Невский проспект, прогулки по каналам.",
    details:
      "Петербург — культурная столица России с множеством исторических достопримечательностей и атмосферой романтики.",
    checklist: [
      {
        title: "Посещение Эрмитажа",
        description: "Огромный музей с мировой коллекцией искусства.",
        photo: "/images/ermitage.jpg",
      },
      {
        title: "Прогулка по Невскому проспекту",
        description: "Главная улица города с магазинами и кафе.",
        photo: "/images/nevsky.jpg",
      },
      {
        title: "Поездка на речном трамвайчике",
        description: "Прогулка по каналам и рекам города.",
        photo: "/images/riverboat.jpg",
      },
      {
        title: "Визит в Петропавловскую крепость",
        description: "Исторический центр с музеями и парком.",
        photo: "/images/peterfort.jpg",
      },
    ],
  },
  "zolotoe-kolco": {
    title: "Золотое кольцо России",
    description: "Владимир, Суздаль, Ростов Великий — история и архитектура.",
    details:
      "Золотое кольцо — это древние города с богатой историей, архитектурой и уникальной русской культурой.",
    checklist: [
      {
        title: "Владимирский Успенский собор",
        description: "Знаменитый собор с фресками Андрея Рублева.",
        photo: "/images/vladimir_cathedral.jpg",
      },
      {
        title: "Суздальский кремль",
        description: "Исторический центр города с музеями.",
        photo: "/images/suzdal_kremlin.jpg",
      },
      {
        title: "Ростовский кремль",
        description: "Один из красивейших архитектурных ансамблей России.",
        photo: "/images/rostov_kremlin.jpg",
      },
      {
        title: "Музей деревянного зодчества",
        description: "Коллекция старинных деревянных построек.",
        photo: "/images/wooden_architecture.jpg",
      },
    ],
  },
  // Add the other 11 routes similarly here...
  kavkaz: {
    title: "Кавказские горы",
    description: "Домбай, Эльбрус, горные тропы и горячие источники.",
    details:
      "Кавказские горы — отличное место для любителей природы, горных походов и отдыха на природе.",
    checklist: [
      {
        title: "Подъём на Эльбрус",
        description: "Самая высокая гора Европы, популярное место для альпинизма.",
        photo: "/images/elbrous.jpg",
      },
      {
        title: "Горнолыжный курорт Домбай",
        description: "Зимние виды спорта и красивые пейзажи.",
        photo: "/images/dombay.jpg",
      },
      {
        title: "Поход к водопадам",
        description: "Маршруты с живописными водопадами и горными видами.",
        photo: "/images/waterfalls.jpg",
      },
      {
        title: "Посещение горячих источников",
        description: "Релаксация и здоровье в природных бассейнах.",
        photo: "/images/hotsprings.jpg",
      },
    ],
  },
  "urals": {
    title: "Уральские горы",
    description: "Свердловск, Пермь, красивые горные пейзажи.",
    details:
      "Урал — это одно из самых красивых и разнообразных мест в России, с живописными горами и культурными памятниками.",
    checklist: [
      {
        title: "Гора Ямантау",
        description: "Популярное место для походов и пикников.",
        photo: "/images/yamantau.jpg",
      },
      {
        title: "Каменные реки",
        description: "Уникальные каменные образования в Урале.",
        photo: "/images/stone_rivers.jpg",
      },
    ],
  },
  "volga": {
    title: "Волга",
    description: "Волгоград, Казань, исторические города и природа.",
    details:
      "Волга — величественная река с множеством городов, культурных и природных достопримечательностей.",
    checklist: [
      {
        title: "Волгоградская набережная",
        description: "Прекрасная прогулочная зона на реке.",
        photo: "/images/volgograd.jpg",
      },
      {
        title: "Казанский кремль",
        description: "Уникальная крепость в Казани.",
        photo: "/images/kazan_kremlin.jpg",
      },
    ],
  },
  "siberia": {
    title: "Сибирь",
    description: "Томск, Новосибирск, дикая природа.",
    details:
      "Сибирь — это огромное пространство с природой, которую не встречаешь нигде в мире.",
    checklist: [
      {
        title: "Ледяные пещеры",
        description: "Известные пещеры в Сибири.",
        photo: "/images/ice_caves.jpg",
      },
      {
        title: "Байкал",
        description: "Озеро Байкал — одно из самых глубоких озёр в мире.",
        photo: "/images/baikal.jpg",
      },
    ],
  },
  "kamchatka": {
    title: "Камчатка",
    description: "Вулканы, горячие источники, дикую природу.",
    details:
      "Камчатка — это край, где можно увидеть активные вулканы и дикие, нетронутые уголки природы.",
    checklist: [
      {
        title: "Вулкан Ключевская Сопка",
        description: "Самый высокий вулкан Камчатки.",
        photo: "/images/key_vulkan.jpg",
      },
      {
        title: "Горячие источники",
        description: "Природные горячие источники в Камчатке.",
        photo: "/images/hotsprings_kamchatka.jpg",
      },
    ],
  },
  "baltic": {
    title: "Балтийский регион",
    description: "Калининград, Латвия, Литва.",
    details:
      "Балтика — это исторический регион с культурным наследием, великолепной архитектурой и красивыми побережьями.",
    checklist: [
      {
        title: "Калининградская крепость",
        description: "Историческое сооружение с музеями.",
        photo: "/images/kaliningrad_fort.jpg",
      },
      {
        title: "Куршская коса",
        description: "Уникальная природная зона.",
        photo: "/images/kosa.jpg",
      },
    ],
  },
  "vladivostok": {
    title: "Владивосток",
    description: "Красивый приморский город с уникальной атмосферой.",
    details:
      "Владивосток — это город на Дальнем Востоке России с уникальной природой и морскими видами.",
    checklist: [
      {
        title: "Мост через бухту Золотой Рог",
        description: "Известный мост, соединяющий два берега.",
        photo: "/images/golden_horn_bridge.jpg",
      },
      {
        title: "Маяк Токаревского",
        description: "Маяк на острове, путь к которому лежит через море.",
        photo: "/images/mayak_tokarevskogo.jpg",
      },
    ],
  },
  "kamchatka-vulkan": {
    title: "Вулканы Камчатки",
    description: "Земля огня, горячие источники.",
    details:
      "Камчатка славится своими активными вулканами и природными горячими источниками.",
    checklist: [
      {
        title: "Гора Вулкан Шивелуч",
        description: "Активный вулкан Камчатки.",
        photo: "/images/shiveluch.jpg",
      },
      {
        title: "Гейзеры в Долине Гейзеров",
        description: "Долина, полная вулканических гейзеров.",
        photo: "/images/geysers.jpg",
      },
    ],
  },
  "sochi": {
    title: "Сочи",
    description: "Черноморское побережье, олимпийские объекты.",
    details:
      "Сочи — это город на Черноморском побережье, известный своими курортами и олимпийскими объектами.",
    checklist: [
      {
        title: "Олимпийский парк",
        description: "Объекты Олимпиады 2014 года.",
        photo: "/images/sochi_olympic.jpg",
      },
      {
        title: "Гора Ахун",
        description: "Прекрасные виды на Сочи и побережье.",
        photo: "/images/akhun_mountain.jpg",
      },
    ]
}
};
