
import streamlit.components.v1 as components
def ver_sql(query: str, key: str):
    # Escapamos cualquier backtick para no romper la template literal JS
    safe_query = query.strip().replace("`", "\\`")
    html = f"""
    <div>
      <button id="show-{key}" style="
        background:none;
        border:none;
        cursor:pointer;
        color:#3366ff;
        font-size:16px;
      ">📝 Ver SQL</button>
    </div>
    <script>
    (function() {{
      const query = `{safe_query}`;
      document.getElementById("show-{key}").onclick = function() {{
        const p = window.parent.document;
        // Si ya existe, no hacemos nada
        if (p.getElementById("sql-backdrop-{key}")) return;

        // Creamos el fondo semitransparente
        const backdrop = p.createElement("div");
        backdrop.id = "sql-backdrop-{key}";
        backdrop.style.cssText =
          "position:fixed;top:0;left:0;width:100%;height:100%;" +
          "background:rgba(0,0,0,0.5);z-index:9998;";
        p.body.appendChild(backdrop);

        // Creamos el modal
        const modal = p.createElement("div");
        modal.id = "sql-modal-{key}";
        modal.style.cssText =
          "position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);" +
          "background:#fff;padding:20px;border-radius:8px;" +
          "box-shadow:0 4px 20px rgba(0,0,0,0.3);" +
          "z-index:9999;max-width:80vw;max-height:80vh;overflow:auto;";
        
        // Pre con la consulta
        const pre = p.createElement("pre");
        pre.textContent = query;
        pre.style.cssText =
          "background:#f5f5f5;padding:10px;border-radius:6px;" +
          "font-family:monospace;white-space:pre-wrap;margin:0;";
        modal.appendChild(pre);

        // Botón Cerrar
        const btn = p.createElement("button");
        btn.textContent = "Cerrar";
        btn.style.cssText =
          "margin-top:10px;padding:6px 12px;border:none;" +
          "background:#3366ff;color:#fff;border-radius:4px;cursor:pointer;";
        btn.onclick = () => {{ backdrop.remove(); modal.remove(); }};
        modal.appendChild(btn);

        p.body.appendChild(modal);
      }};
    }})();
    </script>
    """
    # Iframe muy pequeño que solo muestra el botón
    components.html(html, height=40, width=120, scrolling=False)

