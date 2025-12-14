// Données initiales du blog
let blogData = {
    posts: [
        {
            id: 1,
            title: "Introduction à Bootstrap 5",
            author: "Marie Dubois",
            date: "15 mars 2023",
            content: "Bootstrap 5 est la dernière version du framework CSS le plus populaire. Elle apporte de nombreuses améliorations, notamment la suppression de la dépendance à jQuery, l'ajout de nouveaux composants et une meilleure accessibilité.",
            tags: ["web", "css", "frontend", "bootstrap"]
        },
        {
            id: 2,
            title: "JavaScript Moderne: ES6+",
            author: "Jean Martin",
            date: "10 mars 2023",
            content: "Les nouvelles fonctionnalités d'ECMAScript 6 et des versions ultérieures ont considérablement amélioré le langage JavaScript. Les arrow functions, les promesses, async/await et les modules ont changé la façon dont nous développons.",
            tags: ["javascript", "programmation", "web"]
        },
        {
            id: 3,
            title: "Thymeleaf: Templates Dynamiques pour Spring",
            author: "Sophie Bernard",
            date: "5 mars 2023",
            content: "Thymeleaf est un moteur de template moderne pour les applications web basées sur Java. Il s'intègre parfaitement avec Spring Boot et permet de créer des vues HTML dynamiques avec une syntaxe naturelle.",
            tags: ["java", "spring", "thymeleaf", "backend"]
        }
    ],
    comments: [
        { id: 1, postId: 1, author: "Paul", date: "16 mars 2023", content: "Excellent article, très clair et bien structuré!" },
        { id: 2, postId: 1, author: "Alice", date: "17 mars 2023", content: "Merci pour ce tutoriel, Bootstrap 5 semble vraiment amélioré." },
        { id: 3, postId: 2, author: "Thomas", date: "12 mars 2023", content: "J'attends avec impatience la suite de cet article sur les promesses!" },
        { id: 4, postId: 3, author: "Laura", date: "7 mars 2023", content: "Thymeleaf est effectivement très pratique avec Spring, merci pour l'article." }
    ],
    tags: ["web", "css", "frontend", "bootstrap", "javascript", "programmation", "java", "spring", "thymeleaf", "backend"]
};

// Simuler l'attribut Thymeleaf th:text
function thymeleafText(elementId, text) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = text;
        element.setAttribute('data-th-text', `${text}`);
    }
}

// Simuler l'attribut Thymeleaf th:if
function thymeleafIf(elementId, condition) {
    const element = document.getElementById(elementId);
    if (element) {
        if (condition) {
            element.style.display = '';
        } else {
            element.style.display = 'none';
        }
        element.setAttribute('data-th-if', condition);
    }
}

// Simuler l'attribut Thymeleaf th:each pour générer des articles
function renderPosts() {
    const postsContainer = document.getElementById('postsContainer');
    // On garde le titre et la note
    const title = postsContainer.querySelector('h3');
    const note = postsContainer.querySelector('.template-note');
    
    // On vide le contenu sauf le titre et la note
    postsContainer.innerHTML = '';
    postsContainer.appendChild(title);
    if (note) postsContainer.appendChild(note);
    
    // On crée un conteneur pour les articles
    const articlesContainer = document.createElement('div');
    articlesContainer.id = 'articlesList';
    
    // On génère chaque article
    blogData.posts.forEach(post => {
        const postElement = document.createElement('article');
        postElement.className = 'blog-post';
        postElement.setAttribute('data-th-each', 'post : ${posts}');
        postElement.innerHTML = `
            <h4>${post.title}</h4>
            <div class="post-meta">
                <i class="bi bi-person-circle"></i> <span class="post-author">${post.author}</span> | 
                <i class="bi bi-calendar3"></i> ${post.date} | 
                <i class="bi bi-chat-left"></i> <span class="comment-count" data-post-id="${post.id}">0</span> commentaire(s)
            </div>
            <p>${post.content}</p>
            <div class="post-tags">
                ${post.tags.map(tag => `<span class="tag" data-th-each="tag : ${post.tags}">${tag}</span>`).join('')}
            </div>
            <div class="mt-3">
                <button class="btn btn-sm btn-outline-primary add-comment-btn" data-post-id="${post.id}">
                    <i class="bi bi-chat-left"></i> Ajouter un commentaire
                </button>
                <button class="btn btn-sm btn-outline-secondary ms-2 view-comments-btn" data-post-id="${post.id}">
                    <i class="bi bi-eye"></i> Voir les commentaires
                </button>
            </div>
            <div class="comments-section mt-3" id="comments-${post.id}" style="display: none;">
                <h6>Commentaires:</h6>
                <div id="comments-list-${post.id}">
                    <!-- Les commentaires seront chargés ici -->
                </div>
                <form class="comment-form mt-3" data-post-id="${post.id}">
                    <div class="input-group">
                        <input type="text" class="form-control" placeholder="Votre nom" required>
                        <input type="text" class="form-control" placeholder="Votre commentaire" required>
                        <button class="btn btn-blog" type="submit">Publier</button>
                    </div>
                </form>
            </div>
        `;
        articlesContainer.appendChild(postElement);
    });
    
    postsContainer.appendChild(articlesContainer);
    updateCommentCounts();
    updateRecentComments();
    updatePopularTags();
    updateStatistics();
    
    // Ajouter les événements pour les boutons
    document.querySelectorAll('.add-comment-btn').forEach(button => {
        button.addEventListener('click', function() {
            const postId = parseInt(this.getAttribute('data-post-id'));
            toggleCommentsSection(postId);
        });
    });
    
    document.querySelectorAll('.view-comments-btn').forEach(button => {
        button.addEventListener('click', function() {
            const postId = parseInt(this.getAttribute('data-post-id'));
            toggleCommentsSection(postId);
            loadCommentsForPost(postId);
        });
    });
    
    document.querySelectorAll('.comment-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const postId = parseInt(this.getAttribute('data-post-id'));
            const inputs = this.querySelectorAll('input');
            const author = inputs[0].value;
            const content = inputs[1].value;
            
            if (author && content) {
                addComment(postId, author, content);
                inputs[0].value = '';
                inputs[1].value = '';
            }
        });
    });
}

// Basculer l'affichage de la section des commentaires
function toggleCommentsSection(postId) {
    const commentsSection = document.getElementById(`comments-${postId}`);
    if (commentsSection.style.display === 'none') {
        commentsSection.style.display = 'block';
    } else {
        commentsSection.style.display = 'none';
    }
}

// Charger les commentaires pour un article
function loadCommentsForPost(postId) {
    const commentsList = document.getElementById(`comments-list-${postId}`);
    const postComments = blogData.comments.filter(comment => comment.postId === postId);
    
    if (postComments.length === 0) {
        commentsList.innerHTML = '<p class="text-muted">Aucun commentaire pour le moment. Soyez le premier à commenter!</p>';
        return;
    }
    
    commentsList.innerHTML = postComments.map(comment => `
        <div class="comment">
            <div class="d-flex justify-content-between">
                <span class="comment-author">${comment.author}</span>
                <span class="comment-date">${comment.date}</span>
            </div>
            <p class="mb-0 mt-2">${comment.content}</p>
        </div>
    `).join('');
}

// Ajouter un nouveau commentaire
function addComment(postId, author, content) {
    const newComment = {
        id: blogData.comments.length + 1,
        postId: postId,
        author: author,
        date: new Date().toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }),
        content: content
    };
    
    blogData.comments.push(newComment);
    loadCommentsForPost(postId);
    updateCommentCounts();
    updateRecentComments();
    updateStatistics();
}

// Mettre à jour le nombre de commentaires pour chaque article
function updateCommentCounts() {
    blogData.posts.forEach(post => {
        const commentCount = blogData.comments.filter(comment => comment.postId === post.id).length;
        const countElements = document.querySelectorAll(`.comment-count[data-post-id="${post.id}"]`);
        countElements.forEach(element => {
            element.textContent = commentCount;
        });
    });
}

// Mettre à jour les commentaires récents dans la sidebar
function updateRecentComments() {
    const recentCommentsContainer = document.getElementById('recentComments');
    const recentComments = [...blogData.comments]
        .sort((a, b) => new Date(b.date) - new Date(a.date))
        .slice(0, 3);
    
    if (recentComments.length === 0) {
        recentCommentsContainer.innerHTML = '<p class="text-muted small">Aucun commentaire récent</p>';
        return;
    }
    
    recentCommentsContainer.innerHTML = recentComments.map(comment => {
        const post = blogData.posts.find(p => p.id === comment.postId);
        return `
            <div class="mb-3 pb-3 border-bottom">
                <div class="d-flex justify-content-between">
                    <span class="small fw-bold">${comment.author}</span>
                    <span class="small text-muted">${comment.date}</span>
                </div>
                <p class="small mb-1">${comment.content.substring(0, 60)}...</p>
                <a href="#" class="small text-primary view-post-link" data-post-id="${comment.postId}">Voir l'article: ${post ? post.title.substring(0, 30) : ''}...</a>
            </div>
        `;
    }).join('');
    
    // Ajouter les événements pour les liens
    document.querySelectorAll('.view-post-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = parseInt(this.getAttribute('data-post-id'));
            toggleCommentsSection(postId);
            loadCommentsForPost(postId);
            
            // Faire défiler jusqu'à l'article
            const postElement = document.querySelector(`.add-comment-btn[data-post-id="${postId}"]`).closest('.blog-post');
            postElement.scrollIntoView({ behavior: 'smooth' });
        });
    });
}

// Mettre à jour les tags populaires
function updatePopularTags() {
    const popularTagsContainer = document.getElementById('popularTags');
    
    // Compter les occurrences de chaque tag
    const tagCounts = {};
    blogData.posts.forEach(post => {
        post.tags.forEach(tag => {
            tagCounts[tag] = (tagCounts[tag] || 0) + 1;
        });
    });
    
    // Trier les tags par popularité
    const sortedTags = Object.keys(tagCounts).sort((a, b) => tagCounts[b] - tagCounts[a]).slice(0, 8);
    
    popularTagsContainer.innerHTML = sortedTags.map(tag => 
        `<span class="tag mb-2" style="font-size: 0.9rem;">${tag} <span class="badge bg-light text-dark">${tagCounts[tag]}</span></span> `
    ).join('');
}

// Mettre à jour les statistiques
function updateStatistics() {
    thymeleafText('postsCount', blogData.posts.length);
    thymeleafText('commentsCount', blogData.comments.length);
}

// Ajouter un nouvel article
function addPost(title, author, content, tags) {
    const newPost = {
        id: blogData.posts.length + 1,
        title: title,
        author: author,
        date: new Date().toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' }),
        content: content,
        tags: tags ? tags.split(',').map(tag => tag.trim()) : []
    };
    
    blogData.posts.unshift(newPost); // Ajouter au début
    renderPosts();
    
    // Mettre à jour les tags globaux
    newPost.tags.forEach(tag => {
        if (!blogData.tags.includes(tag)) {
            blogData.tags.push(tag);
        }
    });
}

// Charger des données d'exemple
function loadSampleData() {
    addPost(
        "Les Bases du Développement Web Front-end",
        "Alexandre Petit",
        "Le développement web front-end consiste à créer l'interface utilisateur d'un site web. Les trois technologies de base sont HTML pour la structure, CSS pour le style, et JavaScript pour l'interactivité.",
        "web, frontend, html, css, javascript"
    );
    
    addComment(1, "Nicolas", "Merci pour cette introduction complète!");
    
    alert("Données d'exemple chargées avec succès!");
}

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    // Rendre les articles initiaux
    renderPosts();
    
    // Gérer la soumission du formulaire d'article
    document.getElementById('newPostForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const title = document.getElementById('postTitle').value;
        const author = document.getElementById('postAuthor').value;
        const content = document.getElementById('postContent').value;
        const tags = document.getElementById('postTags').value;
        
        addPost(title, author, content, tags);
        
        // Réinitialiser le formulaire
        this.reset();
        
        // Afficher un message de succès
        alert('Article publié avec succès!');
    });
    
    // Gérer le chargement des données d'exemple
    document.getElementById('loadSampleData').addEventListener('click', loadSampleData);
    
    // Simuler quelques appels Thymeleaf
    thymeleafText('postsCount', blogData.posts.length);
    thymeleafText('commentsCount', blogData.comments.length);
    
    // Démonstration de th:if
    setTimeout(() => {
        thymeleafIf('postsCount', blogData.posts.length > 0);
    }, 100);
});
