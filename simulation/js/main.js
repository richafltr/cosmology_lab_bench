/**
 * Main Three.js Controller & Simulation Engine.
 */

(function() {
  let scene, camera, renderer, controls;
  let currentEpochIndex = 0;
  let activeEpochGroup = null;
  let universeState = null;
  let isPlaying = false;
  let playTimer = null;

  // DOM Elements
  const container = document.getElementById("canvas-container");
  const timeScrubber = document.getElementById("time-scrubber");
  const dispTime = document.getElementById("disp-time");
  const dispRedshift = document.getElementById("disp-redshift");
  const dispHorizon = document.getElementById("disp-horizon");
  const dispSpin = document.getElementById("disp-spin");
  const epochTitle = document.getElementById("epoch-title");
  const epochDesc = document.getElementById("epoch-desc");
  const epochPhysics = document.getElementById("epoch-physics");
  const epochButtons = document.querySelectorAll(".epoch-btn");
  const btnPlayPause = document.getElementById("btn-play-pause");
  const btnResetCam = document.getElementById("btn-reset-cam");

  function initThree() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x030508);
    scene.fog = new THREE.FogExp2(0x030508, 0.0035);

    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 1000);
    camera.position.set(0, 40, 110);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxDistance = 300;
    controls.minDistance = 20;

    // Background cosmic starfield
    createBackgroundStarfield();

    // Lighting
    const ambLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
    dirLight.position.set(50, 80, 50);
    scene.add(dirLight);

    window.addEventListener("resize", onWindowResize);
  }

  function createBackgroundStarfield() {
    const starCount = 6000;
    const pos = new Float32Array(starCount * 3);
    for (let i = 0; i < starCount; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 800;
      pos[i * 3 + 1] = (Math.random() - 0.5) * 800;
      pos[i * 3 + 2] = (Math.random() - 0.5) * 800;
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
    const mat = new THREE.PointsMaterial({ color: 0x556688, size: 0.8, transparent: true, opacity: 0.5 });
    const starfield = new THREE.Points(geo, mat);
    scene.add(starfield);
  }

  function loadUniverseState() {
    fetch("data/universe_state.json")
      .then(res => res.json())
      .then(data => {
        universeState = data;
        updateUIForEpoch(0);
        switchEpoch(0);
      })
      .catch(err => {
        console.warn("Could not load universe_state.json, using fallback default epochs.", err);
        switchEpoch(0);
      });
  }

  function switchEpoch(index) {
    currentEpochIndex = index;

    if (activeEpochGroup) {
      scene.remove(activeEpochGroup);
    }

    activeEpochGroup = window.EpochVisualizer.createEpoch(index, scene);
    scene.add(activeEpochGroup);

    updateUIForEpoch(index);

    // Update active button state
    epochButtons.forEach(btn => {
      btn.classList.toggle("active", parseInt(btn.dataset.epoch) === index);
    });

    timeScrubber.value = index;
  }

  function updateUIForEpoch(index) {
    if (!universeState || !universeState.epochs || !universeState.epochs[index]) {
      // Fallback display
      dispTime.innerText = `Epoch ${index}`;
      return;
    }

    const epoch = universeState.epochs[index];
    dispTime.innerText = epoch.time_display;
    dispRedshift.innerText = (epoch.redshift_z > 1e6) ? "z → ∞" : `z = ${epoch.redshift_z}`;
    epochTitle.innerText = `Epoch ${epoch.id}: ${epoch.name}`;
    epochDesc.innerText = epoch.description;

    // Physics items
    epochPhysics.innerHTML = "";
    if (epoch.key_physics) {
      for (const [k, v] of Object.entries(epoch.key_physics)) {
        const item = document.createElement("div");
        item.className = "physics-item";
        item.innerHTML = `<strong>${k.replace(/_/g, " ")}:</strong> ${v}`;
        epochPhysics.appendChild(item);
      }
    }
  }

  function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  }

  function animate() {
    requestAnimationFrame(animate);

    if (activeEpochGroup) {
      // Rotate active epoch slightly to show 3D depth and Kerr frame-dragging
      activeEpochGroup.rotation.y += 0.003;
      
      const vortex = activeEpochGroup.getObjectByName("vortex_points");
      if (vortex) {
        vortex.rotation.y += 0.006;
      }

      const earth = activeEpochGroup.getObjectByName("earth_globe");
      if (earth) {
        earth.rotation.y += 0.008;
      }
      const cont = activeEpochGroup.getObjectByName("earth_continents");
      if (cont) {
        cont.rotation.y += 0.008;
      }
    }

    controls.update();
    renderer.render(scene, camera);
  }

  // Event Listeners
  timeScrubber.addEventListener("input", function(e) {
    const val = parseFloat(e.target.value);
    const closestEpoch = Math.round(val);
    if (closestEpoch !== currentEpochIndex) {
      switchEpoch(closestEpoch);
    }
  });

  epochButtons.forEach(btn => {
    btn.addEventListener("click", function() {
      const ep = parseInt(this.dataset.epoch);
      switchEpoch(ep);
    });
  });

  btnResetCam.addEventListener("click", function() {
    camera.position.set(0, 40, 110);
    controls.target.set(0, 0, 0);
  });

  btnPlayPause.addEventListener("click", function() {
    isPlaying = !isPlaying;
    if (isPlaying) {
      btnPlayPause.innerText = "Auto Time-Skip: Pause";
      playTimer = setInterval(() => {
        let next = (currentEpochIndex + 1) % 6;
        switchEpoch(next);
      }, 3500);
    } else {
      btnPlayPause.innerText = "Auto Time-Skip: Play";
      clearInterval(playTimer);
    }
  });

  // Startup
  initThree();
  loadUniverseState();
  animate();
})();
