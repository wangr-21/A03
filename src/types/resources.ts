/**
 * 资源类型定义
 */
export interface Resource {
  /**
   * 资源类型（如'图片'、'视频'等）
   */
  type: string;

  /**
   * 资源数据
   */
  data: {
    /**
     * 资源URL
     */
    url: string;

    /**
     * 资源描述
     */
    description?: string;

    /**
     * 资源创建时间
     */
    createdAt?: string;
  };
}
