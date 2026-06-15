/* KigaliFashion - Global JavaScript */

document.addEventListener('DOMContentLoaded', async () => {
  try {
    const res  = await fetch('/api/cart');
    const data = await res.json();
    updateCartBadge(data.cart_count);
  } catch (e) {}

  const hamburger = document.getElementById('hamburger');
  const navLinks  = document.getElementById('nav-links');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
  }

  document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
    if (btn.id === 'detail-add-btn') return;
    btn.addEventListener('click', () => {
      addToCart(btn.dataset.id, btn.dataset.name, 1);
    });
  });
});


async function addToCart(productId, productName, quantity = 1) {
  try {
    const response = await fetch('/cart/add', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ product_id: productId, quantity: quantity }),
    });

    const data = await response.json();

    if (data.success) {
      showToast('✅ ' + data.message);
      updateCartBadge(data.cart_count);
    } else {
      showToast('❌ ' + (data.message || 'Something went wrong.'));
    }

  } catch (err) {
    showToast('❌ Network error. Please try again.');
  }
}

window.addToCart = addToCart;


function updateCartBadge(count) {
  const badge = document.getElementById('cart-badge');
  if (!badge) return;
  badge.textContent = count;
  badge.style.display = count > 0 ? 'flex' : 'none';
}

window.updateCartBadge = updateCartBadge;


let toastTimer = null;

function showToast(message) {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    toast.classList.remove('show');
  }, 2500);
}

window.showToast = showToast;