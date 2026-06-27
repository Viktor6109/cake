document.addEventListener('DOMContentLoaded', function () {

    /* ── Helpers ── */

    function isNewRow(row) {
        var preview = row.querySelector('.field-media_preview');
        if (!preview) return true;
        return !preview.querySelector('img, video');
    }

    /* Returns the direct parent of .inline-related items (fieldset or similar) */
    function getContainer(group) {
        var first = group.querySelector('.inline-related');
        return first ? first.parentElement : null;
    }

    /* Hides file inputs for saved rows; adds "Изменить файл" toggle */
    function initSavedRow(row) {
        var imageField = row.querySelector('.field-image');
        var videoField = row.querySelector('.field-video');
        if (!imageField && !videoField) return;

        if (imageField) imageField.style.display = 'none';
        if (videoField) videoField.style.display = 'none';

        var changeBtn = document.createElement('button');
        changeBtn.type = 'button';
        changeBtn.textContent = 'Изменить файл';
        changeBtn.className = 'inline-action-btn';

        var open = false;
        changeBtn.addEventListener('click', function () {
            open = !open;
            if (imageField) imageField.style.display = open ? '' : 'none';
            if (videoField) videoField.style.display = open ? '' : 'none';
            changeBtn.textContent = open ? 'Скрыть' : 'Изменить файл';
        });

        var preview = row.querySelector('.field-media_preview');
        if (preview) preview.after(changeBtn);
    }

    /* Adds a visible "Удалить" button wired to Django's DELETE checkbox */
    function addDeleteButton(row) {
        var deleteCheckbox = row.querySelector('input[type="checkbox"][id$="-DELETE"]');
        if (!deleteCheckbox) return;

        deleteCheckbox.style.display = 'none';
        var nativeWrap = deleteCheckbox.closest('.field-box, p, div.delete, span.delete');
        if (nativeWrap) nativeWrap.style.display = 'none';

        var deleteBtn = document.createElement('button');
        deleteBtn.type = 'button';
        deleteBtn.textContent = 'Удалить';
        deleteBtn.className = 'inline-action-btn inline-delete-btn';

        deleteBtn.addEventListener('click', function () {
            if (confirm('Удалить этот медиафайл?')) {
                deleteCheckbox.checked = true;
                row.style.opacity = '0.4';
                row.style.pointerEvents = 'none';
                deleteBtn.textContent = 'Будет удалено при сохранении';
                deleteBtn.disabled = true;
            }
        });

        var preview = row.querySelector('.field-media_preview');
        var anchor = preview || row.querySelector('fieldset');
        if (anchor) anchor.after(deleteBtn);
    }

    /* Moves unsaved (new/empty) rows before the first saved row */
    function moveNewRowsToTop(container) {
        var all = Array.from(container.querySelectorAll(':scope > .inline-related:not(.empty-form)'));
        var firstSaved = all.find(function (r) { return !isNewRow(r); });
        if (!firstSaved) return;
        all.filter(isNewRow).forEach(function (row) {
            container.insertBefore(row, firstSaved);
        });
    }

    /* ── Init each inline group ── */

    document.querySelectorAll('.inline-group').forEach(function (group) {
        var container = getContainer(group);
        if (!container) return;

        /* Init saved rows */
        container.querySelectorAll(':scope > .inline-related:not(.empty-form)').forEach(function (row) {
            if (!isNewRow(row)) {
                initSavedRow(row);
                addDeleteButton(row);
            }
        });

        /* Move empty (extra) rows to top */
        moveNewRowsToTop(container);

        /* Watch the real container for new rows added by "Add another" */
        var obs = new MutationObserver(function (mutations) {
            mutations.forEach(function (m) {
                m.addedNodes.forEach(function (node) {
                    if (node.nodeType !== 1) return;
                    if (!node.classList.contains('inline-related')) return;
                    if (node.classList.contains('empty-form')) return;

                    /* Move new empty row to top */
                    var firstSaved = Array.from(
                        container.querySelectorAll(':scope > .inline-related:not(.empty-form)')
                    ).find(function (r) { return !isNewRow(r); });

                    if (firstSaved) container.insertBefore(node, firstSaved);

                    setTimeout(function () {
                        node.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 60);
                });
            });
        });

        obs.observe(container, { childList: true });
    });
});
