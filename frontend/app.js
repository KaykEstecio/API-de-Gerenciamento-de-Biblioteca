const API_URL = 'http://127.0.0.1:8000/api/v1';
let token = localStorage.getItem('token');

function togglePassword(id) {
    const input = document.getElementById(id);
    const icon = input.nextElementSibling.querySelector('i');
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Elements
const authSection = document.getElementById('auth-section');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const tabLogin = document.getElementById('tab-login');
const tabRegister = document.getElementById('tab-register');

const booksSection = document.getElementById('books-section');
const ordersSection = document.getElementById('orders-section');
const booksGrid = document.getElementById('books-grid');
const searchInput = document.getElementById('search-input');
const logoutBtn = document.getElementById('logout-btn');
const navMenu = document.getElementById('nav-menu');
const userInfo = document.getElementById('user-info');

// Navigation
const navBooks = document.getElementById('nav-books');
const navOrders = document.getElementById('nav-orders');
const navAdmin = document.getElementById('nav-admin');

navBooks?.addEventListener('click', (e) => {
    e.preventDefault();
    booksSection.classList.remove('hidden');
    ordersSection.classList.add('hidden');
    document.getElementById('admin-section')?.classList.add('hidden');
    
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    navBooks.classList.add('active');
});

navOrders?.addEventListener('click', (e) => {
    e.preventDefault();
    booksSection.classList.add('hidden');
    ordersSection.classList.remove('hidden');
    document.getElementById('admin-section')?.classList.add('hidden');
    
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    navOrders.classList.add('active');
    loadOrders();
});

navAdmin?.addEventListener('click', (e) => {
    e.preventDefault();
    booksSection.classList.add('hidden');
    ordersSection.classList.add('hidden');
    document.getElementById('admin-section')?.classList.remove('hidden');
    
    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
    navAdmin.classList.add('active');
    loadAdminBooks();
});

// Live Search
searchInput.addEventListener('input', (e) => {
    const term = e.target.value.toLowerCase();
    const cards = booksGrid.querySelectorAll('.book-card');
    cards.forEach(card => {
        const title = card.querySelector('h3').innerText.toLowerCase();
        const author = card.querySelector('.author').innerText.toLowerCase();
        card.style.display = (title.includes(term) || author.includes(term)) ? 'flex' : 'none';
    });
});

// Init
if (token) {
    showDashboard();
}

// Toggle Tabs
tabLogin.addEventListener('click', () => {
    tabLogin.classList.add('active');
    tabRegister.classList.remove('active');
    loginForm.classList.remove('hidden');
    registerForm.classList.add('hidden');
});

tabRegister.addEventListener('click', () => {
    tabRegister.classList.add('active');
    tabLogin.classList.remove('active');
    registerForm.classList.remove('hidden');
    loginForm.classList.add('hidden');
});

// Login Flow
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const msg = document.getElementById('login-msg');
    const btn = document.getElementById('login-submit-btn');
    
    msg.innerText = '';
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Entrando...';

    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    try {
        const response = await fetch(`${API_URL}/auth/token`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Falha no login');
        }
        
        const data = await response.json();
        token = data.access_token;
        localStorage.setItem('token', token);
        showDashboard();
    } catch (err) {
        msg.innerText = err.message;
        btn.disabled = false;
        btn.innerHTML = '<span>Entrar</span>';
    }
});

// Register Flow
registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('reg-name').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;
    const msg = document.getElementById('reg-msg');
    const btn = document.getElementById('reg-submit-btn');
    
    msg.innerText = '';
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Criando conta...';

    try {
        const response = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                full_name: name,
                email: email, 
                password: password,
                is_active: true
            })
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.detail || 'Erro ao cadastrar');
        }
        
        alert('Cadastro realizado! Agora faça login.');
        btn.disabled = false;
        btn.innerHTML = '<span>Criar Conta</span>';
        tabLogin.click();
    } catch (err) {
        msg.innerText = err.message;
        btn.disabled = false;
        btn.innerHTML = '<span>Criar Conta</span>';
    }
});


logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('token');
    token = null;
    authSection.classList.remove('hidden');
    booksSection.classList.add('hidden');
    ordersSection.classList.add('hidden');
    document.getElementById('admin-section')?.classList.add('hidden');
    logoutBtn.classList.add('hidden');
    navMenu.classList.add('hidden');
    userInfo.classList.add('hidden');
    navAdmin.classList.add('hidden');
    location.reload();
});

async function showDashboard() {
    authSection.classList.add('hidden');
    booksSection.classList.remove('hidden');
    ordersSection.classList.remove('hidden');
    logoutBtn.classList.remove('hidden');
    navMenu.classList.remove('hidden');
    userInfo.classList.remove('hidden');
    
    // Verificar se é admin e obter dados do usuário
    try {
        const response = await fetch(`${API_URL}/auth/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const user = await response.json();
        
        // Exibir nome do usuário
        document.getElementById('user-display').innerText = user.full_name || user.email;
        
        if (user.is_superuser) {
            navAdmin.classList.remove('hidden');
            document.getElementById('admin-section').classList.remove('hidden');
            loadAdminBooks();
        }
    } catch (err) {
        console.error('Erro ao verificar perfil');
    }
    
    loadBooks();
    loadOrders();
}

// Admin Panel Variables
const adminSection = document.getElementById('admin-section');
const bookFormContainer = document.getElementById('book-form-container');
const bookForm = document.getElementById('book-form');
const addBookBtn = document.getElementById('add-book-btn');
const cancelFormBtn = document.getElementById('cancel-form-btn');
let editingBookId = null;

// Admin: Show Form
addBookBtn?.addEventListener('click', () => {
    editingBookId = null;
    document.getElementById('form-title').innerText = 'Adicionar Livro';
    bookForm.reset();
    bookFormContainer.classList.remove('hidden');
});

cancelFormBtn?.addEventListener('click', () => {
    bookFormContainer.classList.add('hidden');
    bookForm.reset();
});

// Admin: Submit Form
bookForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const bookData = {
        title: document.getElementById('book-title').value,
        author: document.getElementById('book-author').value,
        description: document.getElementById('book-description').value || null,
        price: parseFloat(document.getElementById('book-price').value),
        stock_quantity: parseInt(document.getElementById('book-stock').value)
    };

    try {
        const url = editingBookId ? `${API_URL}/books/${editingBookId}` : `${API_URL}/books/`;
        const method = editingBookId ? 'PATCH' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookData)
        });

        if (!response.ok) throw new Error('Erro ao salvar livro');
        
        alert(editingBookId ? 'Livro atualizado!' : 'Livro criado!');
        bookFormContainer.classList.add('hidden');
        bookForm.reset();
        loadAdminBooks();
        loadBooks();
    } catch (err) {
        alert(err.message);
    }
});

// Admin: Load Books Table
async function loadAdminBooks() {
    try {
        const response = await fetch(`${API_URL}/books/`);
        const books = await response.json();
        
        const table = document.getElementById('admin-books-table');
        table.innerHTML = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Título</th>
                        <th>Autor</th>
                        <th>Preço</th>
                        <th>Estoque</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    ${books.map(book => `
                        <tr>
                            <td>#${book.id}</td>
                            <td>${book.title}</td>
                            <td>${book.author}</td>
                            <td>R$ ${book.price.toFixed(2)}</td>
                            <td>${book.stock_quantity}</td>
                            <td class="table-actions">
                                <button class="btn-icon" onclick="editBook(${book.id})">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="btn-icon delete" onclick="deleteBook(${book.id})">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    } catch (err) {
        console.error('Erro ao carregar livros admin');
    }
}

// Admin: Edit Book
async function editBook(id) {
    try {
        const response = await fetch(`${API_URL}/books/${id}`);
        const book = await response.json();
        
        editingBookId = id;
        document.getElementById('form-title').innerText = 'Editar Livro';
        document.getElementById('book-title').value = book.title;
        document.getElementById('book-author').value = book.author;
        document.getElementById('book-description').value = book.description || '';
        document.getElementById('book-price').value = book.price;
        document.getElementById('book-stock').value = book.stock_quantity;
        
        bookFormContainer.classList.remove('hidden');
    } catch (err) {
        alert('Erro ao carregar livro');
    }
}

// Admin: Delete Book
async function deleteBook(id) {
    if (!confirm('Tem certeza que deseja excluir este livro?')) return;
    
    try {
        const response = await fetch(`${API_URL}/books/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!response.ok) throw new Error('Erro ao excluir');
        
        alert('Livro excluído!');
        loadAdminBooks();
        loadBooks();
    } catch (err) {
        alert(err.message);
    }
}

async function loadBooks() {
    try {
        const response = await fetch(`${API_URL}/books/`);
        const books = await response.json();
        
        booksGrid.innerHTML = books.map(book => {
            const stockClass = book.stock_quantity <= 0 ? 'stock-out' : 
                               book.stock_quantity <= 3 ? 'stock-low' : 'stock-in';
            const stockLabel = book.stock_quantity <= 0 ? 'Esgotado' : 
                               book.stock_quantity <= 3 ? 'Últimas unidades' : 'Em estoque';

            return `
                <div class="book-card">
                    <h3>${book.title}</h3>
                    <span class="author">por ${book.author}</span>
                    <div class="card-footer">
                        <span class="price-tag">R$ ${book.price.toFixed(2)}</span>
                        <span class="stock-status ${stockClass}">${stockLabel}</span>
                    </div>
                    <button onclick="buyBook(${book.id})" class="buy-btn" ${book.stock_quantity <= 0 ? 'disabled' : ''}>
                        ${book.stock_quantity <= 0 ? 'Esgotado' : 'Comprar Agora'}
                    </button>
                </div>
            `;
        }).join('');
    } catch (err) {
        console.error('Erro ao carregar livros');
    }
}

async function loadOrders() {
    try {
        const response = await fetch(`${API_URL}/orders/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const orders = await response.json();
        
        const container = document.getElementById('orders-list');
        container.className = 'orders-container';
        
        if (orders.length === 0) {
            container.innerHTML = '<p class="subtitle">Você ainda não realizou pedidos.</p>';
            return;
        }

        container.innerHTML = orders.map(order => {
            const total = order.items.reduce((sum, item) => sum + (item.item_price * item.quantity), 0);
            const itemsList = order.items.map(item => 
                `<li>${item.quantity}x ${item.book.title} - R$ ${(item.item_price * item.quantity).toFixed(2)}</li>`
            ).join('');

            return `
                <div class="order-card">
                    <div class="order-info">
                        <h4>Pedido #${String(order.id).padStart(4, '0')}</h4>
                        <span class="order-date">Criado em: ${new Date(order.created_at).toLocaleDateString()}</span>
                        <div class="order-items">
                            <strong>Itens:</strong>
                            <ul style="margin: 5px 0 0 20px; color: rgba(255,255,255,0.7);">
                                ${itemsList}
                            </ul>
                            <strong style="margin-top: 10px; display: block;">Total: R$ ${total.toFixed(2)}</strong>
                        </div>
                    </div>
                    <div class="order-actions">
                        <span class="status-badge status-${order.status}">
                            ${order.status === 'pending' ? 'Pendente' : 'Pago'}
                        </span>
                        ${order.status === 'pending' ? `
                            <button onclick="payOrder(${order.id})" class="pay-min-btn">Pagar</button>
                        ` : ''}
                    </div>
                </div>
            `;
        }).join('');
    } catch (err) {
        console.error('Erro ao carregar pedidos');
    }
}

async function buyBook(bookId) {
    try {
        const response = await fetch(`${API_URL}/orders/`, {
            method: 'POST',
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ items: [{ book_id: bookId, quantity: 1 }] })
        });
        
        if (!response.ok) {
            const data = await response.json();
            alert(data.detail);
        } else {
            alert('Pedido realizado com sucesso!');
            loadBooks();
            loadOrders();
        }
    } catch (err) {
        alert(err.message);
    }
}

let currentOrderId = null;

async function payOrder(orderId) {
    currentOrderId = orderId;
    
    // Buscar detalhes do pedido
    try {
        const response = await fetch(`${API_URL}/orders/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const orders = await response.json();
        const order = orders.find(o => o.id === orderId);
        
        if (!order) {
            alert('Pedido não encontrado');
            return;
        }
        
        // Calcular total
        const total = order.items.reduce((sum, item) => sum + (item.item_price * item.quantity), 0);
        
        // Preencher detalhes no modal
        const detailsHtml = `
            <p><strong>Pedido:</strong> #${String(order.id).padStart(4, '0')}</p>
            <p><strong>Itens:</strong> ${order.items.length}</p>
            <p><strong>Total:</strong> R$ ${total.toFixed(2)}</p>
        `;
        
        document.getElementById('payment-order-details').innerHTML = detailsHtml;
        document.getElementById('payment-modal').classList.remove('hidden');
    } catch (err) {
        alert('Erro ao carregar pedido');
    }
}

function closePaymentModal() {
    document.getElementById('payment-modal').classList.add('hidden');
    currentOrderId = null;
}

async function confirmPayment() {
    if (!currentOrderId) return;
    
    const selectedMethod = document.querySelector('input[name="payment-method"]:checked').value;
    const methodNames = {
        'credit': 'Cartão de Crédito',
        'pix': 'PIX',
        'boleto': 'Boleto Bancário'
    };
    
    try {
        const response = await fetch(`${API_URL}/orders/${currentOrderId}/pay`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (!response.ok) throw new Error('Erro ao processar pagamento');
        
        closePaymentModal();
        
        // Mostrar mensagem de sucesso
        const successMsg = document.createElement('div');
        successMsg.className = 'payment-success';
        successMsg.innerHTML = `
            <i class="fas fa-check-circle"></i>
            <h3>Pagamento Confirmado!</h3>
            <p>Método: ${methodNames[selectedMethod]}</p>
        `;
        document.body.appendChild(successMsg);
        
        setTimeout(() => {
            successMsg.remove();
        }, 3000);
        
        loadOrders();
    } catch (err) {
        alert(err.message);
    }
}
