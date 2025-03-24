class CommentManager {
    constructor(options) {
        this.options = options;
        this.csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; // For Auth
        this.initEventListeners();
    }

    initEventListeners() {
        // main comment form submission
        document.getElementById('comment-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            const content = document.getElementById('comment-content').value;
            this.submitComment(content);
        });

        // reply button handlers
        document.querySelectorAll('.reply-btn').forEach(button => {
            button.addEventListener('click', () => {
                const commentId = button.dataset.commentId;
                document.querySelectorAll('.reply-form').forEach(form => form.style.display = 'none');
                document.getElementById(`reply-form-${commentId}`).style.display = 'block';
            });
        });

        // cancel reply handlers
        document.querySelectorAll('.cancel-reply').forEach(button => {
            button.addEventListener('click', () => {
                button.closest('.reply-form').style.display = 'none';
            });
        });

        // submit reply handlers
        document.querySelectorAll('.submit-reply').forEach(button => {
            button.addEventListener('click', () => {
                const commentId = button.dataset.commentId;
                const content = button.closest('.reply-form').querySelector('textarea').value;
                this.submitComment(content, commentId);
            });
        });
    }

    submitComment(content, parentId = null) {
        fetch(this.options.submitUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken,
            },
            body: JSON.stringify({
                content: content,
                parent_id: parentId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const comment = this.createCommentElement(data.comment);
                if (parentId) {
                    document.getElementById(`replies-${parentId}`).appendChild(comment);
                    document.getElementById(`reply-form-${parentId}`).style.display = 'none';
                    document.getElementById(`reply-form-${parentId}`).querySelector('textarea').value = '';
                } else {
                    document.getElementById('comments-container').insertBefore(
                        comment,
                        document.getElementById('comments-container').firstChild
                    );
                    document.getElementById('comment-content').value = '';
                }
            }
        });
    }

    createCommentElement(comment) {
        const div = document.createElement('div');
        div.className = comment.parent_id ? 'reply' : 'comment';
        div.id = `comment-${comment.id}`;
        div.innerHTML = `
            <div class="comment-header">
                <strong>${comment.username}</strong>
                <small>just now</small>
            </div>
            <div class="comment-content">
                ${comment.content}
            </div>
            ${comment.parent_id ? '' : `
                <div class="comment-actions">
                    <button class="btn btn-sm btn-link reply-btn" data-comment-id="${comment.id}">Reply</button>
                </div>
                <div class="reply-form" id="reply-form-${comment.id}" style="display: none;">
                    <textarea class="form-control mb-2" rows="2"></textarea>
                    <button class="btn btn-sm btn-primary submit-reply" data-comment-id="${comment.id}">Submit Reply</button>
                    <button class="btn btn-sm btn-secondary cancel-reply">Cancel</button>
                </div>
                <div class="replies" id="replies-${comment.id}"></div>
            `}
        `;

        if (!comment.parent_id) {
            setTimeout(() => {
                this.attachEventListenersToComment(div);
            }, 0);
        }

        return div;
    }

    attachEventListenersToComment(commentElement) {
        const replyBtn = commentElement.querySelector('.reply-btn');
        const submitReplyBtn = commentElement.querySelector('.submit-reply');
        const cancelReplyBtn = commentElement.querySelector('.cancel-reply');

        if (replyBtn) {
            replyBtn.addEventListener('click', () => {
                const commentId = replyBtn.dataset.commentId;
                document.querySelectorAll('.reply-form').forEach(form => form.style.display = 'none');
                document.getElementById(`reply-form-${commentId}`).style.display = 'block';
            });
        }

        if (submitReplyBtn) {
            submitReplyBtn.addEventListener('click', () => {
                const commentId = submitReplyBtn.dataset.commentId;
                const content = submitReplyBtn.closest('.reply-form').querySelector('textarea').value;
                this.submitComment(content, commentId);
            });
        }

        if (cancelReplyBtn) {
            cancelReplyBtn.addEventListener('click', () => {
                cancelReplyBtn.closest('.reply-form').style.display = 'none';
            });
        }
    }
}
