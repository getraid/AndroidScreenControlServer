(window.webpackJsonp=window.webpackJsonp||[]).push([[1],{170:function(e,o,t){var content=t(229);"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,t(78).default)("56b15182",content,!0,{sourceMap:!1})},193:function(e,o,t){"use strict";var c={data:function(){return{checked:!1}},watch:{checked:function(e){e?(document.documentElement.setAttribute("data-theme","dark"),localStorage.setItem("theme","dark")):(document.documentElement.setAttribute("data-theme","light"),localStorage.setItem("theme","light"))}},mounted:function(){this.checked="dark"===localStorage.getItem("theme")}},r=(t(228),t(79)),component=Object(r.a)(c,(function(){var e=this,o=e.$createElement,t=e._self._c||o;return t("div",[t("div",{staticClass:"float-right"},[t("label",{staticClass:"px-1",attrs:{for:"checkbox"}},[e._v("Darkmode:")]),t("input",{directives:[{name:"model",rawName:"v-model",value:e.checked,expression:"checked"}],staticClass:"mr-1 align-middle align-self-center",attrs:{id:"checkbox",type:"checkbox"},domProps:{checked:Array.isArray(e.checked)?e._i(e.checked,null)>-1:e.checked},on:{change:function(o){var t=e.checked,c=o.target,r=!!c.checked;if(Array.isArray(t)){var l=e._i(t,null);c.checked?l<0&&(e.checked=t.concat([null])):l>-1&&(e.checked=t.slice(0,l).concat(t.slice(l+1)))}else e.checked=r}}})]),e._v(" "),t("div",[t("Nuxt")],1)])}),[],!1,null,null,null);o.a=component.exports},194:function(e,o,t){t(195),e.exports=t(196)},228:function(e,o,t){"use strict";t(170)},229:function(e,o,t){(o=t(77)(!1)).push([e.i,":root{--primary-color:#302ae6;--secondary-color:#536390;--font-color:#424242;--bg-color:#eff1ff;--heading-color:#292922;--vartodo:#161616;--vartodo2:#d9e3e3;--varNote:#fff572;--varNoteHighlight:#bfe77e;--varNoteHighlightFocus:#80e77e;--tickbox:#007bff}[data-theme=dark]{--primary-color:#9a97f3;--secondary-color:#818cab;--font-color:#e1e1ff;--bg-color:#161625;--heading-color:#818cab;--vartodo:#d2ee57;--vartodo2:#425a85;--varNote:#e2d95c;--varNoteHighlight:#ebd097;--varNoteHighlightFocus:#cc9b63;--tickbox:#44b17f}body{background-color:#eff1ff;background-color:var(--bg-color);color:#424242;color:var(--font-color)}",""]),e.exports=o}},[[194,6,2,7]]]);