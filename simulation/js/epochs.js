/**
 * Epoch visual generator for Three.js 3D Cosmological Evolution Simulation.
 * Generates distinct meshes, particle systems, and shader visualizers for each epoch.
 */

window.EpochVisualizer = (function() {
  function createEpoch0_Bounce(scene) {
    const group = new THREE.Group();
    group.name = "epoch_0";

    // 1. Central Kerr Black Hole Horizon Sphere (Black with glowing accretion/ergosphere)
    const horizonGeo = new THREE.SphereGeometry(18, 64, 64);
    const horizonMat = new THREE.MeshBasicMaterial({ color: 0x010206 });
    const horizon = new THREE.Mesh(horizonGeo, horizonMat);
    group.add(horizon);

    // 2. Ergosphere & Frame-Dragging Ring
    const ergoGeo = new THREE.RingGeometry(22, 38, 64);
    const ergoMat = new THREE.MeshBasicMaterial({
      color: 0xff3300,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.75
    });
    const ergoRing = new THREE.Mesh(ergoGeo, ergoMat);
    ergoRing.rotation.x = Math.PI / 2.3;
    group.add(ergoRing);

    // 3. Torsion Spin Vortex Particles
    const count = 4000;
    const pos = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const colorA = new THREE.Color(0xff4500);
    const colorB = new THREE.Color(0xffffff);

    for (let i = 0; i < count; i++) {
      const radius = 20 + Math.random() * 80;
      const theta = Math.random() * Math.PI * 2;
      const height = (Math.random() - 0.5) * (120 - radius * 0.8);

      pos[i * 3] = Math.cos(theta) * radius;
      pos[i * 3 + 1] = height;
      pos[i * 3 + 2] = Math.sin(theta) * radius;

      const mixed = colorA.clone().lerp(colorB, Math.random() * 0.5);
      colors[i * 3] = mixed.r;
      colors[i * 3 + 1] = mixed.g;
      colors[i * 3 + 2] = mixed.b;
    }

    const partGeo = new THREE.BufferGeometry();
    partGeo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    partGeo.setAttribute("color", new THREE.BufferAttribute(colors, 3));
    const partMat = new THREE.PointsMaterial({
      size: 1.8,
      vertexColors: true,
      transparent: true,
      opacity: 0.85
    });
    const vortex = new THREE.Points(partGeo, partMat);
    vortex.name = "vortex_points";
    group.add(vortex);

    return group;
  }

  function createEpoch1_CosmicDawn(scene) {
    const group = new THREE.Group();
    group.name = "epoch_1";

    // Neutral hydrogen cloud fog particles
    const count = 3500;
    const pos = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const colGas = new THREE.Color(0x3a1505);
    const colStar = new THREE.Color(0xffeedd);

    for (let i = 0; i < count; i++) {
      const r = Math.random() * 120;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);

      pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      pos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      pos[i * 3 + 2] = r * Math.cos(phi);

      const isPopIII = Math.random() < 0.08;
      const c = isPopIII ? colStar : colGas;
      colors[i * 3] = c.r;
      colors[i * 3 + 1] = c.g;
      colors[i * 3 + 2] = c.b;
    }

    const geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    geo.setAttribute("color", new THREE.BufferAttribute(colors, 3));
    const mat = new THREE.PointsMaterial({ size: 2.2, vertexColors: true, transparent: true, opacity: 0.7 });
    group.add(new THREE.Points(geo, mat));

    return group;
  }

  function createEpoch2_MoMz14(scene) {
    const group = new THREE.Group();
    group.name = "epoch_2";

    // MoM-z14: Ultra-compact, intense starburst galaxy core (r_e = 74 pc)
    const coreGeo = new THREE.SphereGeometry(12, 32, 32);
    const coreMat = new THREE.MeshBasicMaterial({ color: 0x88ccff });
    const core = new THREE.Mesh(coreGeo, coreMat);
    group.add(core);

    // Nitrogen-enriched ionized nebular glow (N IV], N III] emission)
    const haloGeo = new THREE.SphereGeometry(26, 32, 32);
    const haloMat = new THREE.MeshBasicMaterial({
      color: 0x00ffff,
      transparent: true,
      opacity: 0.35,
      wireframe: true
    });
    group.add(new THREE.Mesh(haloGeo, haloMat));

    // Surrounding starburst cluster particles
    const count = 2500;
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const r = Math.pow(Math.random(), 2.0) * 80;
      const th = Math.random() * Math.PI * 2;
      const ph = Math.acos(2 * Math.random() - 1);
      pos[i * 3] = r * Math.sin(ph) * Math.cos(th);
      pos[i * 3 + 1] = r * Math.sin(ph) * Math.sin(th) * 0.4;
      pos[i * 3 + 2] = r * Math.cos(ph);
    }
    const pGeo = new THREE.BufferGeometry();
    pGeo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    const pMat = new THREE.PointsMaterial({ color: 0x99ddff, size: 2.0, transparent: true, opacity: 0.8 });
    group.add(new THREE.Points(pGeo, pMat));

    return group;
  }

  function createEpoch3_JADES(scene) {
    const group = new THREE.Group();
    group.name = "epoch_3";

    // Display spiral galaxies with 60:40 clockwise parity alignment
    const numGalaxies = 40;
    for (let g = 0; g < numGalaxies; g++) {
      const isCW = g < 24; // 60% clockwise
      const spiralGroup = new THREE.Group();

      const armCount = 2;
      const pointsPerArm = 60;
      const pos = new Float32Array(armCount * pointsPerArm * 3);
      let idx = 0;

      for (let a = 0; a < armCount; a++) {
        const armOffset = a * Math.PI;
        for (let p = 0; p < pointsPerArm; p++) {
          const r = 2 + (p / pointsPerArm) * 16;
          const theta = (isCW ? 1 : -1) * (p * 0.25) + armOffset;
          pos[idx++] = Math.cos(theta) * r;
          pos[idx++] = (Math.random() - 0.5) * 1.5;
          pos[idx++] = Math.sin(theta) * r;
        }
      }

      const geo = new THREE.BufferGeometry();
      geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
      const mat = new THREE.PointsMaterial({
        color: isCW ? 0x00e5ff : 0xff77aa,
        size: 1.5,
        transparent: true,
        opacity: 0.85
      });
      spiralGroup.add(new THREE.Points(geo, mat));

      // Spread spirals along cosmic filament
      const dist = 30 + Math.random() * 120;
      const angle = (g / numGalaxies) * Math.PI * 2;
      spiralGroup.position.set(Math.cos(angle) * dist, (Math.random() - 0.5) * 60, Math.sin(angle) * dist);
      spiralGroup.rotation.x = (Math.random() - 0.5) * 0.8;
      spiralGroup.rotation.z = (Math.random() - 0.5) * 0.8;
      group.add(spiralGroup);
    }

    return group;
  }

  function createEpoch4_XLSSC122(scene) {
    const group = new THREE.Group();
    group.name = "epoch_4";

    // 1. Hyper-concentrated Dark Matter Core (NFW profile, c200 = 6.3)
    const coreGeo = new THREE.SphereGeometry(30, 32, 32);
    const coreMat = new THREE.MeshBasicMaterial({
      color: 0x113366,
      transparent: true,
      opacity: 0.35,
      wireframe: true
    });
    group.add(new THREE.Mesh(coreGeo, coreMat));

    // 2. Giant Gravitational Lensing Blue Arcs (Einstein Ring at theta_E = 4.1 arcsec)
    for (let arc = 0; arc < 3; arc++) {
      const arcAngleStart = (arc * (Math.PI * 2 / 3)) + 0.3;
      const arcCurve = new THREE.EllipseCurve(0, 0, 50, 50, arcAngleStart, arcAngleStart + 0.9, false, 0);
      const points = arcCurve.getPoints(50);
      const arcGeo = new THREE.BufferGeometry().setFromPoints(points);
      const arcMat = new THREE.LineBasicMaterial({ color: 0x00e5ff, linewidth: 3 });
      const arcLine = new THREE.Line(arcGeo, arcMat);
      arcLine.rotation.x = Math.PI / 2;
      group.add(arcLine);
    }

    // 3. Intracluster Light (ICL) diffuse starlight
    const count = 2000;
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const r = Math.pow(Math.random(), 1.5) * 65;
      const th = Math.random() * Math.PI * 2;
      const ph = Math.acos(2 * Math.random() - 1);
      pos[i * 3] = r * Math.sin(ph) * Math.cos(th);
      pos[i * 3 + 1] = r * Math.sin(ph) * Math.sin(th) * 0.6;
      pos[i * 3 + 2] = r * Math.cos(ph);
    }
    const pGeo = new THREE.BufferGeometry();
    pGeo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    const pMat = new THREE.PointsMaterial({ color: 0xffcc88, size: 1.6, transparent: true, opacity: 0.7 });
    group.add(new THREE.Points(pGeo, pMat));

    return group;
  }

  function createEpoch5_ModernHumans(scene) {
    const group = new THREE.Group();
    group.name = "epoch_5";

    // 1. Earth - Blue Marble with atmosphere
    const earthGeo = new THREE.SphereGeometry(16, 48, 48);
    const earthMat = new THREE.MeshPhongMaterial({
      color: 0x1155cc,
      emissive: 0x051533,
      specular: 0x333333,
      shininess: 25
    });
    const earth = new THREE.Mesh(earthGeo, earthMat);
    earth.name = "earth_globe";
    group.add(earth);

    // Atmosphere halo
    const atmoGeo = new THREE.SphereGeometry(18, 32, 32);
    const atmoMat = new THREE.MeshBasicMaterial({
      color: 0x00aaff,
      transparent: true,
      opacity: 0.25,
      side: THREE.BackSide
    });
    group.add(new THREE.Mesh(atmoGeo, atmoMat));

    // Continents indicator
    const contCount = 1200;
    const pos = new Float32Array(contCount * 3);
    for (let i = 0; i < contCount; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(2 * Math.random() - 1);
      const r = 16.2;
      pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      pos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      pos[i * 3 + 2] = r * Math.cos(phi);
    }
    const cGeo = new THREE.BufferGeometry();
    cGeo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    const cMat = new THREE.PointsMaterial({ color: 0x22aa55, size: 1.8 });
    const continents = new THREE.Points(cGeo, cMat);
    continents.name = "earth_continents";
    group.add(continents);

    // Human satellite / radio sphere
    const satRingGeo = new THREE.RingGeometry(25, 26, 64);
    const satRingMat = new THREE.MeshBasicMaterial({ color: 0x00e5ff, side: THREE.DoubleSide, transparent: true, opacity: 0.4 });
    const satRing = new THREE.Mesh(satRingGeo, satRingMat);
    satRing.rotation.x = Math.PI / 3;
    group.add(satRing);

    return group;
  }

  return {
    createEpoch: function(id, scene) {
      switch (id) {
        case 0: return createEpoch0_Bounce(scene);
        case 1: return createEpoch1_CosmicDawn(scene);
        case 2: return createEpoch2_MoMz14(scene);
        case 3: return createEpoch3_JADES(scene);
        case 4: return createEpoch4_XLSSC122(scene);
        case 5: return createEpoch5_ModernHumans(scene);
        default: return createEpoch0_Bounce(scene);
      }
    }
  };
})();
