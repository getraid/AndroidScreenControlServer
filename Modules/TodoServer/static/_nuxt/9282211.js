(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{170:function(e,c,o){var content=o(229);"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,o(79).default)("56b15182",content,!0,{sourceMap:!1})},193:function(e,c,o){"use strict";var t={data:function(){return{checked:!1}},watch:{checked:function(e){e?(document.documentElement.setAttribute("data-theme","dark"),localStorage.setItem("theme","dark")):(document.documentElement.setAttribute("data-theme","light"),localStorage.setItem("theme","light"))}},mounted:function(){this.checked="dark"===localStorage.getItem("theme")}},r=(o(228),o(96)),component=Object(r.a)(t,(function(){var e=this,c=e.$createElement,o=e._self._c||c;return o("div",[o("div",{staticClass:"float-right"},[o("label",{staticClass:"px-1",attrs:{for:"checkbox"}},[e._v("Darkmode:")]),o("input",{directives:[{name:"model",rawName:"v-model",value:e.checked,expression:"checked"}],staticClass:"mr-1 align-middle align-self-center",attrs:{id:"checkbox",type:"checkbox"},domProps:{checked:Array.isArray(e.checked)?e._i(e.checked,null)>-1:e.checked},on:{change:function(c){var o=e.checked,t=c.target,r=!!t.checked;if(Array.isArray(o)){var l=e._i(o,null);t.checked?l<0&&(e.checked=o.concat([null])):l>-1&&(e.checked=o.slice(0,l).concat(o.slice(l+1)))}else e.checked=r}}})]),e._v(" "),o("div",[o("Nuxt")],1)])}),[],!1,null,null,null);c.a=component.exports},194:function(e,c,o){o(195),e.exports=o(196)},228:function(e,c,o){"use strict";o(170)},229:function(e,c,o){(c=o(78)(!1)).push([e.i,":root{--primary-color:#302ae6;--secondary-color:#536390;--font-color:#424242;--bg-color:#fff;--heading-color:#292922;--vartodo:#161616;--vartodo2:#d9e3e3;--tickbox:#007bff}[data-theme=dark]{--primary-color:#9a97f3;--secondary-color:#818cab;--font-color:#e1e1ff;--bg-color:#161625;--heading-color:#818cab;--vartodo:#d2ee57;--vartodo2:#425a85;--tickbox:#44b17f}body{background-color:#fff;background-color:var(--bg-color);color:#424242;color:var(--font-color)}",""]),e.exports=c}},[[194,3,1,4]]]);