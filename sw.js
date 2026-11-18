// Samo da bi klik na obaveštenje vratio na stranu (i da Android uopšte prikaže obaveštenje).
self.addEventListener("notificationclick", (e) => {
  e.notification.close();
  e.waitUntil(clients.matchAll({ type: "window" }).then((cs) => cs.length ? cs[0].focus() : clients.openWindow("./")));
});
